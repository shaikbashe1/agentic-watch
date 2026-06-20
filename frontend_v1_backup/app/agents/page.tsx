"use client";

import { useActivities, useAgentStats } from "@/hooks/useApi";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from "recharts";
import { Activity } from "@/types";

const AGENT_COLORS: Record<string, string> = {
  CoderAgent: "#3b82f6",
  PlannerAgent: "#8b5cf6",
  ResearchAgent: "#10b981",
  TesterAgent: "#f59e0b",
};

function agentColor(name: string) {
  return AGENT_COLORS[name] ?? "#6b7280";
}

export default function AgentsPage() {
  const { data: agentStats = [], isLoading } = useAgentStats();
  const { data: activities = [] } = useActivities(200);

  // Per-agent breakdown: total, success, blocked, warning
  const agentDetails = agentStats.map((a) => {
    const acts = activities.filter((act: Activity) => act.agent_name === a.agent_name);
    const success = acts.filter((act: Activity) => act.status === "success").length;
    const blocked = acts.filter((act: Activity) => act.status === "blocked").length;
    const warning = acts.filter((act: Activity) => act.status === "warning").length;
    const avgRisk = acts.filter((act: Activity) => act.risk_score != null).reduce((sum, act) => sum + (act.risk_score ?? 0), 0)
      / (acts.filter((act: Activity) => act.risk_score != null).length || 1);
    return { ...a, success, blocked, warning, avgRisk: Math.round(avgRisk) };
  });

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Multi-Agent Monitoring</h1>
      <p className="text-muted-foreground">Track and compare activity across all registered AI agents.</p>

      {isLoading && <div>Loading...</div>}

      {/* Summary cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {agentDetails.map((a) => (
          <Card key={a.agent_name} style={{ borderLeftColor: agentColor(a.agent_name), borderLeftWidth: 4 }}>
            <CardHeader className="pb-2">
              <CardTitle className="text-base">{a.agent_name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-1 text-sm">
              <div className="flex justify-between">
                <span>Total Actions</span>
                <span className="font-bold">{a.total}</span>
              </div>
              <div className="flex justify-between">
                <span>Success</span>
                <span className="text-green-600 font-medium">{a.success}</span>
              </div>
              <div className="flex justify-between">
                <span>Warnings</span>
                <span className="text-yellow-600 font-medium">{a.warning}</span>
              </div>
              <div className="flex justify-between">
                <span>Blocked</span>
                <span className="text-red-600 font-medium">{a.blocked}</span>
              </div>
              <div className="flex justify-between">
                <span>Avg Risk</span>
                <span className={a.avgRisk >= 70 ? "text-red-600 font-bold" : "font-medium"}>{a.avgRisk}</span>
              </div>
            </CardContent>
          </Card>
        ))}
        {agentDetails.length === 0 && !isLoading && (
          <div className="col-span-4 text-center text-muted-foreground py-8">
            No agents tracked yet. Create activities with different agent_name values.
          </div>
        )}
      </div>

      {/* Comparison chart */}
      {agentDetails.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Agent Activity Comparison</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentDetails}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="agent_name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Legend />
                <Bar dataKey="success" fill="#22c55e" name="Success" />
                <Bar dataKey="warning" fill="#eab308" name="Warning" />
                <Bar dataKey="blocked" fill="#ef4444" name="Blocked" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Recent activity per agent */}
      {agentDetails.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Recent Activities by Agent</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Agent</TableHead>
                  <TableHead>Action</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Policy</TableHead>
                  <TableHead>Risk</TableHead>
                  <TableHead>Timestamp</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {activities.slice(0, 20).map((a: Activity) => (
                  <TableRow key={a.id}>
                    <TableCell>
                      <span className="font-medium" style={{ color: agentColor(a.agent_name) }}>
                        {a.agent_name}
                      </span>
                    </TableCell>
                    <TableCell><code className="text-xs">{a.action_type}</code></TableCell>
                    <TableCell>
                      <Badge variant={a.status === "success" ? "default" : a.status === "blocked" ? "destructive" : "secondary"}>
                        {a.status}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      {a.policy_decision ? (
                        <Badge variant={a.policy_decision === "block" ? "destructive" : a.policy_decision === "warn" ? "secondary" : "outline"}>
                          {a.policy_decision}
                        </Badge>
                      ) : "—"}
                    </TableCell>
                    <TableCell>
                      {a.risk_score != null ? (
                        <span className={a.risk_score >= 70 ? "text-red-600 font-bold" : ""}>{a.risk_score}</span>
                      ) : "—"}
                    </TableCell>
                    <TableCell className="text-xs">{new Date(a.timestamp).toLocaleString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
