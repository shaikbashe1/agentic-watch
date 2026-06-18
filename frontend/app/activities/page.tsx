"use client";

import { useActivities } from "@/hooks/useApi";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Activity } from "@/types";

function statusVariant(s: string) {
  if (s === "success") return "default" as const;
  if (s === "blocked") return "destructive" as const;
  if (s === "warning") return "secondary" as const;
  return "outline" as const;
}

function decisionVariant(d: string) {
  if (d === "block") return "destructive" as const;
  if (d === "warn") return "secondary" as const;
  return "outline" as const;
}

export default function ActivitiesPage() {
  const { data: activities = [], isLoading, error } = useActivities();
  const [search, setSearch] = useState("");
  const [filterAgent, setFilterAgent] = useState("all");

  const agentNames = [...new Set(activities.map((a: Activity) => a.agent_name))];

  const filtered = activities.filter((a: Activity) => {
    const matchSearch =
      a.agent_name.toLowerCase().includes(search.toLowerCase()) ||
      a.action_type.toLowerCase().includes(search.toLowerCase()) ||
      a.action_description.toLowerCase().includes(search.toLowerCase());
    const matchAgent = filterAgent === "all" || a.agent_name === filterAgent;
    return matchSearch && matchAgent;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold tracking-tight">Activity Logs (Audit Trail)</h1>
        <Badge variant="outline">{filtered.length} record{filtered.length !== 1 ? "s" : ""}</Badge>
      </div>
      <div className="flex gap-3 flex-wrap">
        <Input
          placeholder="Search by agent, action, or description..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="max-w-sm"
        />
        <select
          value={filterAgent}
          onChange={(e) => setFilterAgent(e.target.value)}
          className="border rounded px-3 py-2 text-sm bg-white"
        >
          <option value="all">All Agents</option>
          {agentNames.map((n) => <option key={n} value={n}>{n}</option>)}
        </select>
      </div>

      {error && <div className="text-red-500">Failed to load activities. Is the backend running?</div>}

      <div className="border rounded-md bg-white overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Timestamp</TableHead>
              <TableHead>Agent</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Resource</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Policy</TableHead>
              <TableHead>Risk</TableHead>
              <TableHead>Alignment</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={9} className="text-center py-4">Loading...</TableCell></TableRow>
            ) : filtered.length === 0 ? (
              <TableRow><TableCell colSpan={9} className="text-center py-4 text-muted-foreground">No activities found</TableCell></TableRow>
            ) : filtered.map((activity: Activity) => (
              <TableRow key={activity.id}>
                <TableCell className="text-xs whitespace-nowrap">{new Date(activity.timestamp).toLocaleString()}</TableCell>
                <TableCell className="font-medium">{activity.agent_name}</TableCell>
                <TableCell><code className="text-xs">{activity.action_type}</code></TableCell>
                <TableCell className="max-w-xs truncate">{activity.action_description}</TableCell>
                <TableCell>{activity.target_resource}</TableCell>
                <TableCell>
                  <Badge variant={statusVariant(activity.status)}>{activity.status}</Badge>
                </TableCell>
                <TableCell>
                  {activity.policy_decision ? (
                    <Badge variant={decisionVariant(activity.policy_decision)}>{activity.policy_decision}</Badge>
                  ) : "—"}
                </TableCell>
                <TableCell>
                  {activity.risk_score != null ? (
                    <span className={activity.risk_score >= 70 ? "text-red-600 font-bold" : "text-gray-700"}>
                      {activity.risk_score}
                    </span>
                  ) : "—"}
                </TableCell>
                <TableCell>
                  {activity.alignment_score != null ? (
                    <span className={activity.alignment_score < 40 ? "text-orange-600 font-bold" : "text-gray-700"}>
                      {activity.alignment_score}
                    </span>
                  ) : "—"}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
