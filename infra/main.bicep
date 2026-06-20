@description('Location for all resources.')
param location string = resourceGroup().location

@description('Environment name to prefix resources.')
param environmentName string = 'agenticwatch'

@description('PostgreSQL Administrator Login')
param pgAdminLogin string = 'agentwatchadmin'

@description('PostgreSQL Administrator Password')
@secure()
param pgAdminPassword string

@description('Container Registry Server')
param acrServer string

@description('Container Registry Username')
param acrUsername string

@description('Container Registry Password')
@secure()
param acrPassword string

@description('Frontend Image Tag')
param frontendImage string = 'ghcr.io/shaikbashe1/agentic-watch-frontend:latest'

@description('Backend Image Tag')
param backendImage string = 'ghcr.io/shaikbashe1/agentic-watch-backend:latest'

// Shared variables
var logAnalyticsWorkspaceName = '${environmentName}-laws'
var appInsightsName = '${environmentName}-appins'
var containerAppEnvName = '${environmentName}-env'
var redisName = '${environmentName}-redis'
var postgresServerName = '${environmentName}-pg'
var postgresDatabaseName = 'agentwatch'

// Log Analytics Workspace
resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsWorkspaceName
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// Application Insights
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: appInsightsName
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalytics.id
  }
}

// Redis Cache
resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: redisName
  location: location
  properties: {
    sku: {
      name: 'Basic'
      family: 'C'
      capacity: 0
    }
  }
}

// PostgreSQL Flexible Server
resource postgresServer 'Microsoft.DBforPostgreSQL/flexibleServers@2023-03-01-preview' = {
  name: postgresServerName
  location: location
  sku: {
    name: 'Standard_B1ms'
    tier: 'Burstable'
  }
  properties: {
    version: '15'
    administratorLogin: pgAdminLogin
    administratorLoginPassword: pgAdminPassword
    storage: {
      storageSizeGB: 32
    }
    highAvailability: {
      mode: 'Disabled'
    }
  }
}

resource postgresDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2023-03-01-preview' = {
  parent: postgresServer
  name: postgresDatabaseName
}

// Allow Azure services to access Postgres
resource postgresFirewallRule 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2023-03-01-preview' = {
  parent: postgresServer
  name: 'AllowAzureServices'
  properties: {
    startIpAddress: '0.0.0.0'
    endIpAddress: '0.0.0.0'
  }
}

// Container Apps Environment
resource containerAppEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: containerAppEnvName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

// ClickHouse Container App
resource clickhouseApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${environmentName}-clickhouse'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: false
        targetPort: 8123
      }
    }
    template: {
      containers: [
        {
          name: 'clickhouse'
          image: 'clickhouse/clickhouse-server:24.3'
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
          env: [
            {
              name: 'CLICKHOUSE_USER'
              value: 'default'
            }
            {
              name: 'CLICKHOUSE_PASSWORD'
              value: ''
            }
            {
              name: 'CLICKHOUSE_DB'
              value: 'agentwatch'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}

// OTel Collector Container App
resource collectorApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${environmentName}-collector'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 4318
      }
    }
    template: {
      containers: [
        {
          name: 'otel-collector'
          image: 'otel/opentelemetry-collector-contrib:0.110.0'
          command: ['--config=/etc/otel-collector-config.yaml']
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          // Note: Needs the config mounted or built into custom image. For simplicity, assuming default or external config mapping.
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
      }
    }
  }
}

// Backend (FastAPI) Container App
resource backendApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${environmentName}-backend'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
      registries: [
        {
          server: acrServer
          username: acrUsername
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: acrPassword
        }
        {
          name: 'database-url'
          value: 'postgresql+asyncpg://${pgAdminLogin}:${pgAdminPassword}@${postgresServer.name}.postgres.database.azure.com:5432/${postgresDatabaseName}'
        }
        {
          name: 'redis-url'
          value: 'redis://:${redisCache.listKeys().primaryKey}@${redisCache.properties.hostName}:${redisCache.properties.sslPort}/0'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'backend'
          image: backendImage
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
          env: [
            {
              name: 'DATABASE_URL'
              secretRef: 'database-url'
            }
            {
              name: 'REDIS_URL'
              secretRef: 'redis-url'
            }
            {
              name: 'CLICKHOUSE_URL'
              value: 'http://${clickhouseApp.name}:8123'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
      }
    }
  }
}

// Celery Worker Container App
resource workerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${environmentName}-worker'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      registries: [
        {
          server: acrServer
          username: acrUsername
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: acrPassword
        }
        {
          name: 'database-url'
          value: 'postgresql+asyncpg://${pgAdminLogin}:${pgAdminPassword}@${postgresServer.name}.postgres.database.azure.com:5432/${postgresDatabaseName}'
        }
        {
          name: 'redis-url'
          value: 'redis://:${redisCache.listKeys().primaryKey}@${redisCache.properties.hostName}:${redisCache.properties.sslPort}/0'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'worker'
          image: backendImage
          command: [
            'celery'
            '-A'
            'app.core.celery_app'
            'worker'
            '--loglevel=info'
          ]
          resources: {
            cpu: json('1.0')
            memory: '2.0Gi'
          }
          env: [
            {
              name: 'DATABASE_URL'
              secretRef: 'database-url'
            }
            {
              name: 'REDIS_URL'
              secretRef: 'redis-url'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
      }
    }
  }
}

// Frontend (Next.js) Container App
resource frontendApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${environmentName}-frontend'
  location: location
  properties: {
    managedEnvironmentId: containerAppEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 3000
      }
      registries: [
        {
          server: acrServer
          username: acrUsername
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: acrPassword
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'frontend'
          image: frontendImage
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          env: [
            {
              name: 'NEXT_PUBLIC_API_URL'
              value: 'https://${backendApp.properties.configuration.ingress.fqdn}'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 5
      }
    }
  }
}

output frontendUrl string = frontendApp.properties.configuration.ingress.fqdn
output backendUrl string = backendApp.properties.configuration.ingress.fqdn
output collectorUrl string = collectorApp.properties.configuration.ingress.fqdn
