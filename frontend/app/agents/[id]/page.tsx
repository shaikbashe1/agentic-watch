"use client"

import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { PlayCircle, Activity, ShieldCheck, History } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

const mockRuns = [
  { id: "run_8fa29", status: "Success", duration: "1.2s", cost: "$0.004", risk: 12, time: "2 mins ago" },
  { id: "run_7fa28", status: "Success", duration: "2.4s", cost: "$0.012", risk: 8, time: "15 mins ago" },
  { id: "run_6fa27", status: "Blocked", duration: "0.1s", cost: "$0.000", risk: 95, time: "1 hour ago" },
]

export default function AgentDetail() {
  const { id } = useParams()

  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">Customer Support Bot</h1>
            <Badge className="bg-green-600 hover:bg-green-700">Healthy</Badge>
          </div>
          <p className="text-muted-foreground mt-2 font-mono text-sm">ID: {id} | Version: 2.1.0 | Framework: LangChain</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="border-neutral-700">
            <ShieldCheck className="h-4 w-4 mr-2" /> View Policies
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            <PlayCircle className="h-4 w-4 mr-2" /> Test Agent
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="border-neutral-800 bg-black/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">Success Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-400">99.2%</div>
            <p className="text-xs text-muted-foreground mt-1">Last 24 hours</p>
          </CardContent>
        </Card>
        <Card className="border-neutral-800 bg-black/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">Avg Latency</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">1,250ms</div>
            <p className="text-xs text-muted-foreground mt-1">-5% from yesterday</p>
          </CardContent>
        </Card>
        <Card className="border-neutral-800 bg-black/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">Avg Cost / Run</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$0.008</div>
            <p className="text-xs text-muted-foreground mt-1">Primarily GPT-4o</p>
          </CardContent>
        </Card>
        <Card className="border-neutral-800 bg-black/40">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-muted-foreground">Active Sessions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-400">42</div>
            <p className="text-xs text-muted-foreground mt-1">Currently executing</p>
          </CardContent>
        </Card>
      </div>

      <Card className="border-neutral-800 bg-black/40 mt-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <History className="h-5 w-5" /> Recent Runs
          </CardTitle>
          <CardDescription>Latest executions for this specific agent.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Run ID</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Duration</TableHead>
                <TableHead>Cost</TableHead>
                <TableHead>Risk Score</TableHead>
                <TableHead>Time</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockRuns.map((run) => (
                <TableRow key={run.id} className="border-neutral-800">
                  <TableCell className="font-mono text-sm text-blue-400">{run.id}</TableCell>
                  <TableCell>
                    <Badge variant={run.status === "Success" ? "default" : "destructive"} className={run.status === "Success" ? "bg-green-600" : "bg-red-600"}>
                      {run.status}
                    </Badge>
                  </TableCell>
                  <TableCell>{run.duration}</TableCell>
                  <TableCell className="font-mono">{run.cost}</TableCell>
                  <TableCell>
                    <span className={run.risk > 50 ? "text-red-400 font-bold" : "text-green-400 font-bold"}>{run.risk}</span>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{run.time}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
