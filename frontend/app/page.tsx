"use client";
import React, { useEffect, useState } from "react";

import { useStats, useActivities, useAlerts, useAgentStats } from "@/hooks/useApi";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, AlertTriangle, Shield, ShieldAlert, CheckCircle, Users } from "lucide-react";
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar, LineChart, Line, Legend,
} from "recharts";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";

function severityVariant(s: string) {
  if (s === "critical") return "destructive";
  if (s === "high") return "destructive";
  return "secondary";
}

function statusVariant(s: string) {
  if (s === "success") return "default";
  if (s === "blocked") return "destructive";
  if (s === "warning") return "secondary";
  return "outline";
}

import { useQueryClient } from "@tanstack/react-query";

export default function Dashboard() {
  const queryClient = useQueryClient();
  const { data: stats } = useStats();
  const { data: activities = [] } = useActivities(20);
  const { data: alerts = [] } = useAlerts(20);
  const { data: agentStats = [] } = useAgentStats();

  // Setup WebSocket for Real-Time Dashboard Updates
  useEffect(() => {
    const token = localStorage.getItem('agentwatch_token');
    if (token) {
        const ws = new WebSocket(`ws://localhost:8000/ws/dashboard?token=${token}`);
        ws.onmessage = (event) => {
            try {
                // Instantly refresh TanStack queries on new events
                queryClient.invalidateQueries({ queryKey: ["stats"] });
                queryClient.invalidateQueries({ queryKey: ["activities"] });
                queryClient.invalidateQueries({ queryKey: ["alerts"] });
            } catch (e) { console.error(e); }
        };
        return () => ws.close();
    }
  }, [queryClient]);

  // Activity volume by status (last 10 activities, most recent last)
  const activityData = [...activities].reverse().slice(0, 10).map((a, i) => ({
    name: `#${i + 1}`,
    success: a.status === "success" ? 1 : 0,
    warning: a.status === "warning" ? 1 : 0,
    blocked: a.status === "blocked" ? 1 : 0,
  }));

  // Risk trend from activities that have a risk_score
  const riskData = [...activities]
    .filter((a) => a.risk_score != null)
    .reverse()
    .slice(0, 10)
    .map((a, i) => ({
      name: a.action_type.slice(0, 10),
      risk: a.risk_score ?? 0,
      alignment: a.alignment_score ?? 0,
    }));

  const criticalAlerts = alerts.filter((a) => a.severity === "critical").length;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Overview Dashboard</h1>

      {/* Stat cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Actions</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total ?? 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Safe Actions</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.success ?? 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Warnings</CardTitle>
            <AlertTriangle className="h-4 w-4 text-yellow-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.warning ?? 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Blocked Actions</CardTitle>
            <Shield className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.blocked ?? 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Alerts</CardTitle>
            <ShieldAlert className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{criticalAlerts}</div>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Activity Volume</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              {(() => {
                const [metrics, setMetrics] = useState({ total_actions: 0, safe_actions: 0, warnings: 0, blocked_actions: 0, critical_alerts: 0 });

                useEffect(() => {
                    // Fetch initial stats
                    fetch('http://localhost:8000/stats')
                        .then(res => res.json())
                        .then(data => setMetrics(data))
                        .catch(err => console.error(err));

                    // Setup WebSocket for Real-Time Dashboard Updates
                    const token = localStorage.getItem('agentwatch_token');
                    if (token) {
                        const ws = new WebSocket(`ws://localhost:8000/ws/dashboard?token=${token}`);
                        ws.onmessage = (event) => {
                            try {
                                const data = JSON.parse(event.data);
                                if (data.event_type === 'tool_call') {
                                    setMetrics(prev => ({ ...prev, total_actions: prev.total_actions + 1, safe_actions: prev.safe_actions + 1 }));
                                } else if (data.event_type === 'alert') {
                                    if (data.payload.severity === 'Critical') {
                                        setMetrics(prev => ({ ...prev, critical_alerts: prev.critical_alerts + 1 }));
                                    }
                                }
                            } catch (e) { console.error(e); }
                        };
                        return () => ws.close();
                    }
                }, []);
                return (
                  <AreaChart data={activityData.length ? activityData : [{ name: "–", success: 0, warning: 0, blocked: 0 }]}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Legend />
                    <Area type="monotone" dataKey="success" stroke="#22c55e" fill="#bbf7d0" stackId="1" />
                    <Area type="monotone" dataKey="warning" stroke="#eab308" fill="#fef08a" stackId="1" />
                    <Area type="monotone" dataKey="blocked" stroke="#ef4444" fill="#fecaca" stackId="1" />
                  </AreaChart>
                )
              })()}
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Risk &amp; Alignment Trend</CardTitle>
          </CardHeader>
          <CardContent className="h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
              {riskData.length ? (
                <LineChart data={riskData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis domain={[0, 100]} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} name="Risk Score" />
                  <Line type="monotone" dataKey="alignment" stroke="#3b82f6" strokeWidth={2} name="Alignment Score" />
                </LineChart>
              ) : (
                <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
                  No alignment data yet. Create activities with a user_goal.
                </div>
              )}
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Multi-agent breakdown */}
      {agentStats.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="h-5 w-5" /> Agent Activity Breakdown
            </CardTitle>
          </CardHeader>
          <CardContent className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={agentStats}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="agent_name" />
                <YAxis allowDecimals={false} />
                <Tooltip />
                <Bar dataKey="total" fill="#3b82f6" name="Actions" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      )}

      {/* Recent tables */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Recent Activities</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Agent</TableHead>
                  <TableHead>Action</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Risk</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {activities.slice(0, 5).map((activity) => (
                  <TableRow key={activity.id}>
                    <TableCell className="font-medium">{activity.agent_name}</TableCell>
                    <TableCell>{activity.action_type}</TableCell>
                    <TableCell>
                      <Badge variant={statusVariant(activity.status)}>{activity.status}</Badge>
                    </TableCell>
                    <TableCell>
                      {activity.risk_score != null ? (
                        <span className={activity.risk_score >= 70 ? "text-red-600 font-bold" : "text-gray-600"}>
                          {activity.risk_score}
                        </span>
                      ) : "—"}
                    </TableCell>
                  </TableRow>
                ))}
                {activities.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center py-4 text-muted-foreground">
                      No activities yet
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Title</TableHead>
                  <TableHead>Severity</TableHead>
                  <TableHead>Status</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {alerts.slice(0, 5).map((alert) => (
                  <TableRow key={alert.id}>
                    <TableCell className="font-medium">{alert.title}</TableCell>
                    <TableCell>
                      <Badge variant={severityVariant(alert.severity)}>{alert.severity}</Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{alert.status}</Badge>
                    </TableCell>
                  </TableRow>
                ))}
                {alerts.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={3} className="text-center py-4 text-muted-foreground">
                      No alerts yet
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
