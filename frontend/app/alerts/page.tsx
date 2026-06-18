"use client";

import { useAlerts, useUpdateAlertStatus } from "@/hooks/useApi";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useState } from "react";
import { Alert } from "@/types";

function severityVariant(s: string) {
  if (s === "critical") return "destructive" as const;
  if (s === "high") return "destructive" as const;
  return "secondary" as const;
}

function severityBorderColor(s: string) {
  if (s === "critical") return "border-l-red-600";
  if (s === "high") return "border-l-orange-500";
  if (s === "medium") return "border-l-yellow-500";
  return "border-l-blue-400";
}

export default function AlertsPage() {
  const { data: alerts = [], isLoading, error } = useAlerts();
  const updateStatus = useUpdateAlertStatus();
  const [search, setSearch] = useState("");
  const [filterSeverity, setFilterSeverity] = useState("all");

  const filtered = alerts.filter((a: Alert) => {
    const matchSearch =
      a.title.toLowerCase().includes(search.toLowerCase()) ||
      (a.description ?? "").toLowerCase().includes(search.toLowerCase()) ||
      a.source.toLowerCase().includes(search.toLowerCase());
    const matchSeverity = filterSeverity === "all" || a.severity === filterSeverity;
    return matchSearch && matchSeverity;
  });

  const handleAcknowledge = (id: number) => {
    updateStatus.mutate({ id, status: "acknowledged" });
  };

  const handleResolve = (id: number) => {
    updateStatus.mutate({ id, status: "resolved" });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Alerts</h1>
        <Badge variant="outline">{filtered.length} alert{filtered.length !== 1 ? "s" : ""}</Badge>
      </div>

      <div className="flex gap-3 flex-wrap">
        <Input
          placeholder="Search alerts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-xs"
        />
        {["all", "critical", "high", "medium", "low"].map((sev) => (
          <Button
            key={sev}
            variant={filterSeverity === sev ? "default" : "outline"}
            size="sm"
            onClick={() => setFilterSeverity(sev)}
          >
            {sev.charAt(0).toUpperCase() + sev.slice(1)}
          </Button>
        ))}
      </div>

      {isLoading && <div className="text-muted-foreground">Loading...</div>}
      {error && <div className="text-red-500">Failed to load alerts. Is the backend running?</div>}

      {!isLoading && filtered.length === 0 && (
        <div className="text-muted-foreground py-8 text-center">No alerts found.</div>
      )}

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filtered.map((alert: Alert) => (
          <Card key={alert.id} className={`border-l-4 ${severityBorderColor(alert.severity)}`}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium truncate max-w-[70%]">{alert.title}</CardTitle>
              <Badge variant={severityVariant(alert.severity)}>{alert.severity}</Badge>
            </CardHeader>
            <CardContent className="space-y-2">
              {alert.description && (
                <p className="text-sm text-muted-foreground">{alert.description}</p>
              )}
              <div className="flex justify-between items-center text-xs text-muted-foreground">
                <span>Source: {alert.source}</span>
                <Badge variant="outline" className="text-xs">{alert.status}</Badge>
              </div>
              <p className="text-xs text-muted-foreground">
                {new Date(alert.created_at).toLocaleString()}
              </p>
              {alert.status === "open" && (
                <div className="flex gap-2 pt-1">
                  <Button size="sm" variant="outline" onClick={() => handleAcknowledge(alert.id)}>
                    Acknowledge
                  </Button>
                  <Button size="sm" variant="outline" onClick={() => handleResolve(alert.id)}>
                    Resolve
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
