"use client"

import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Bell, AlertTriangle } from "lucide-react"

const mockAlertRules = [
  { id: "ar_1", name: "High Cost Spike", metric: "Cost / Hour", threshold: "> $50", channels: ["Slack", "Email"] },
  { id: "ar_2", name: "Critical Policy Violation", metric: "Policy Actions", threshold: "BLOCK > 5/min", channels: ["PagerDuty"] },
  { id: "ar_3", name: "Latency Degradation", metric: "P95 Latency", threshold: "> 5000ms", channels: ["Slack"] },
]

const mockFiredAlerts = [
  { id: "al_1", rule: "High Cost Spike", triggeredAt: "2026-06-19 14:15:00", status: "FIRING", severity: "HIGH" },
  { id: "al_2", rule: "Latency Degradation", triggeredAt: "2026-06-19 10:05:00", status: "RESOLVED", severity: "MEDIUM" },
]

export default function AlertsDashboard() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Alerting & Notifications</h1>
          <p className="text-muted-foreground">Manage your alert rules and view fired incidents.</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
          <Bell className="h-4 w-4 mr-2" /> New Alert Rule
        </Button>
      </div>

      <Card className="border-neutral-800 bg-black/40 border-l-4 border-l-red-500">
        <CardHeader>
          <CardTitle className="text-red-400 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" /> Active Incidents
          </CardTitle>
          <CardDescription>Alerts that are currently firing.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Incident ID</TableHead>
                <TableHead>Rule Triggered</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Triggered At</TableHead>
                <TableHead>Status</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockFiredAlerts.map((alert) => (
                <TableRow key={alert.id} className="border-neutral-800">
                  <TableCell>
                    <Link href={`/alerts/${alert.id}`} className="text-blue-400 hover:underline">
                      {alert.id}
                    </Link>
                  </TableCell>
                  <TableCell className="font-semibold">{alert.rule}</TableCell>
                  <TableCell>
                    <Badge variant="destructive" className={alert.severity === "HIGH" ? "bg-red-500" : "bg-yellow-500"}>
                      {alert.severity}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-mono text-sm">{alert.triggeredAt}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className={alert.status === "FIRING" ? "text-red-400 border-red-500/50" : "text-green-400 border-green-500/50"}>
                      {alert.status}
                    </Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Card className="border-neutral-800 bg-black/40 mt-8">
        <CardHeader>
          <CardTitle>Configured Alert Rules</CardTitle>
          <CardDescription>Rules continuously monitored by the AgentWatch engine.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Rule Name</TableHead>
                <TableHead>Metric</TableHead>
                <TableHead>Threshold</TableHead>
                <TableHead>Notification Channels</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockAlertRules.map((rule) => (
                <TableRow key={rule.id} className="border-neutral-800">
                  <TableCell className="font-semibold">{rule.name}</TableCell>
                  <TableCell>{rule.metric}</TableCell>
                  <TableCell className="font-mono text-xs">{rule.threshold}</TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      {rule.channels.map(ch => (
                        <Badge key={ch} variant="secondary" className="bg-neutral-800">
                          {ch}
                        </Badge>
                      ))}
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
