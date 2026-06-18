"use client";

import { useActivities } from "@/hooks/useApi";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { useState } from "react";
import { Input } from "@/components/ui/input";

export default function ActivitiesPage() {
  const { data: activities = [], isLoading } = useActivities();
  const [search, setSearch] = useState("");

  const filtered = activities.filter(a => 
    a.agent_name.toLowerCase().includes(search.toLowerCase()) ||
    a.action_type.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Activity Logs</h1>
      <div className="flex gap-4">
        <Input 
          placeholder="Search by Agent or Action..." 
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="max-w-sm"
        />
      </div>
      <div className="border rounded-md bg-white">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Timestamp</TableHead>
              <TableHead>Agent</TableHead>
              <TableHead>Action</TableHead>
              <TableHead>Description</TableHead>
              <TableHead>Resource</TableHead>
              <TableHead>Status</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={6} className="text-center py-4">Loading...</TableCell></TableRow>
            ) : filtered.length === 0 ? (
              <TableRow><TableCell colSpan={6} className="text-center py-4">No activities found</TableCell></TableRow>
            ) : filtered.map((activity) => (
              <TableRow key={activity.id}>
                <TableCell>{new Date(activity.timestamp).toLocaleString()}</TableCell>
                <TableCell>{activity.agent_name}</TableCell>
                <TableCell>{activity.action_type}</TableCell>
                <TableCell>{activity.action_description}</TableCell>
                <TableCell>{activity.target_resource}</TableCell>
                <TableCell>
                  <Badge variant={activity.status === 'success' ? 'default' : 'destructive'}>
                    {activity.status}
                  </Badge>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
