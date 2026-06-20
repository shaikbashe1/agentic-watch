"use client";
import React, { useEffect, useState } from "react";

import { useStats, useActivities, useAlerts, useAgentStats, useTokenTimeseries, useCostTimeseries, useLatencyTimeseries } from "@/hooks/useApi";
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
  const { data: tokensTimeseries = [] } = useTokenTimeseries();
  const { data: costsTimeseries = [] } = useCostTimeseries();
  const { data: latencyTimeseries = [] } = useLatencyTimeseries();

  // Store live events for the Live Stream component
  const [liveEvents, setLiveEvents] = useState<any[]>([]);

  // Setup WebSocket for Real-Time Dashboard Updates
  useEffect(() => {
    const token = localStorage.getItem('agentwatch_token');
    if (token) {
        const ws = new WebSocket(`ws://localhost:8000/ws/dashboard?token=${token}`);
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                
                // Add to live stream
                setLiveEvents(prev => {
                    const newEvents = [data, ...prev];
                    return newEvents.slice(0, 50); // Keep last 50
                });

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

      {/* Live Event Stream Panel */}
      <Card className="border-primary/20 shadow-lg shadow-primary/5">
        <CardHeader className="bg-muted/30 border-b border-border py-3">
          <CardTitle className="text-sm font-medium flex items-center gap-2">
            <span className="relative flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
            </span>
            Live Event Stream
          </CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="h-48 overflow-y-auto bg-card p-4 space-y-2 font-mono text-xs">
            {liveEvents.length === 0 ? (
                <div className="text-muted-foreground h-full flex items-center justify-center">Waiting for telemetry...</div>
            ) : (
                liveEvents.map((evt, idx) => (
                    <div key={idx} className="flex gap-4 border-b border-border/50 pb-2">
                        <span className="text-muted-foreground whitespace-nowrap">{new Date(evt.timestamp).toLocaleTimeString()}</span>
                        <Badge variant="outline" className="text-[10px] uppercase">{evt.event_type}</Badge>
                        <span className="text-foreground truncate">{JSON.stringify(evt.payload).substring(0, 100)}...</span>
                    </div>
                ))
            )}
          </div>
        </CardContent>
      </Card>

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
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle>LLM Cost Trend (USD)</CardTitle>
          </CardHeader>
          <CardContent className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              {costsTimeseries.length ? (
                  <AreaChart data={costsTimeseries}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="cost" stroke="#ef4444" fill="#fecaca" />
                  </AreaChart>
              ) : (
                  <div className="flex items-center justify-center h-full text-muted-foreground text-sm">No cost data.</div>
              )}
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Token Usage</CardTitle>
          </CardHeader>
          <CardContent className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              {tokensTimeseries.length ? (
                  <BarChart data={tokensTimeseries}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="tokens" fill="#3b82f6" />
                  </BarChart>
              ) : (
                  <div className="flex items-center justify-center h-full text-muted-foreground text-sm">No token data.</div>
              )}
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Agent Latency (Seconds)</CardTitle>
          </CardHeader>
          <CardContent className="h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              {latencyTimeseries.length ? (
                <LineChart data={latencyTimeseries}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="latency" stroke="#10b981" strokeWidth={2} />
                </LineChart>
              ) : (
                <div className="flex items-center justify-center h-full text-muted-foreground text-sm">No latency data.</div>
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
