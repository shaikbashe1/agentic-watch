"use client";

import { useAlerts } from "@/hooks/useApi";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function AlertsPage() {
  const { data: alerts = [], isLoading } = useAlerts();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isLoading ? (
          <div>Loading...</div>
        ) : alerts.length === 0 ? (
          <div>No alerts found</div>
        ) : alerts.map(alert => (
          <Card key={alert.id} className="border-l-4 border-l-red-500">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">{alert.severity}</CardTitle>
              <Badge variant={alert.severity === 'Critical' ? 'destructive' : 'secondary'}>
                {alert.severity}
              </Badge>
            </CardHeader>
            <CardContent>
              <p className="text-lg font-bold">{alert.message}</p>
              <p className="text-sm text-muted-foreground mt-2">{new Date(alert.timestamp).toLocaleString()}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
