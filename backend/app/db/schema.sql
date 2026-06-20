-- Workspaces (multi-tenant root)
CREATE TABLE workspaces (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    plan TEXT DEFAULT 'free',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Agents registry
CREATE TABLE agents (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name TEXT NOT NULL,
    version TEXT,
    framework TEXT,
    environment TEXT,
    tags JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ
);

-- Events (TimescaleDB hypertable for time-series)
CREATE TABLE events (
    id UUID NOT NULL,
    workspace_id UUID NOT NULL,
    trace_id TEXT NOT NULL,
    span_id TEXT NOT NULL,
    parent_span_id TEXT,
    session_id TEXT NOT NULL,
    agent_id UUID,
    event_type TEXT NOT NULL,
    framework TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    latency_ms INTEGER,
    llm_provider TEXT,
    llm_model TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd DECIMAL(10,8),
    tool_name TEXT,
    risk_score INTEGER,
    policy_decision TEXT,
    error TEXT,
    payload JSONB,
    PRIMARY KEY (id, started_at)
);

SELECT create_hypertable('events', 'started_at');
CREATE INDEX ON events (workspace_id, started_at DESC);
CREATE INDEX ON events (trace_id, started_at);
CREATE INDEX ON events (session_id, started_at);

-- Policies
CREATE TABLE policies (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name TEXT NOT NULL,
    priority INTEGER DEFAULT 100,
    enabled BOOLEAN DEFAULT true,
    conditions JSONB NOT NULL,
    actions JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Policy violations log
CREATE TABLE policy_violations (
    id UUID PRIMARY KEY,
    workspace_id UUID,
    policy_id UUID REFERENCES policies(id),
    event_id UUID,
    trace_id TEXT,
    agent_id UUID,
    action TEXT,
    reason TEXT,
    violated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Alert rules
CREATE TABLE alert_rules (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name TEXT NOT NULL,
    condition JSONB NOT NULL,       -- metric, operator, threshold
    severity TEXT DEFAULT 'warning',
    channels JSONB DEFAULT '[]',    -- slack/email/webhook
    enabled BOOLEAN DEFAULT true
);

-- API keys
CREATE TABLE api_keys (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name TEXT NOT NULL,
    key_hash TEXT UNIQUE NOT NULL,  -- never store plaintext
    key_prefix TEXT NOT NULL,       -- "aw_live_abc..." for display
    scopes TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    revoked BOOLEAN DEFAULT false
);
