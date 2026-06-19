"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Play, Pause, Activity } from "lucide-react"
import { Button } from "@/components/ui/button"

interface TraceEvent {
  id: string
  trace_id: string
  event_type: string
  model: string
  cost: number
  risk_score: number
  latency: number
  time: string
}

export default function TracesFeed() {
  const [events, setEvents] = useState<TraceEvent[]>([])
  const [isLive, setIsLive] = useState(true)

  useEffect(() => {
    // In production, connect to /ws/dashboard or /ws/traces
    // Here we simulate incoming live WebSocket data
    
    let interval: NodeJS.Timeout
    
    if (isLive) {
      interval = setInterval(() => {
        const newEvent: TraceEvent = {
          id: Math.random().toString(36).substr(2, 9),
          trace_id: `trace-${Math.floor(Math.random() * 1000)}`,
          event_type: Math.random() > 0.5 ? "llm_call" : "tool_call",
          model: Math.random() > 0.5 ? "gpt-4o" : "claude-3-5-sonnet",
          cost: Math.random() * 0.05,
          risk_score: Math.floor(Math.random() * 100),
          latency: Math.floor(Math.random() * 2000),
          time: new Date().toLocaleTimeString()
        }
        
        setEvents((prev) => [newEvent, ...prev].slice(0, 50)) // Keep last 50
      }, 2000) // New event every 2 seconds
    }
    
    return () => clearInterval(interval)
  }, [isLive])

  const getRiskColor = (score: number) => {
    if (score > 80) return "bg-red-500"
    if (score > 60) return "bg-orange-500"
    if (score > 30) return "bg-yellow-500"
    return "bg-green-500"
  }

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold flex items-center gap-2">
            Live Trace Feed
            {isLive && <Activity className="h-6 w-6 text-blue-500 animate-pulse" />}
          </h1>
          <p className="text-muted-foreground">Real-time AI agent telemetry across all workspaces.</p>
        </div>
        <Button 
          variant={isLive ? "destructive" : "default"} 
          onClick={() => setIsLive(!isLive)}
          className={isLive ? "bg-red-500/10 text-red-500 hover:bg-red-500/20 border-red-500" : "bg-blue-600 hover:bg-blue-700 text-white"}
        >
          {isLive ? <><Pause className="h-4 w-4 mr-2" /> Pause Feed</> : <><Play className="h-4 w-4 mr-2" /> Resume Feed</>}
        </Button>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Time</TableHead>
                <TableHead>Trace ID</TableHead>
                <TableHead>Event Type</TableHead>
                <TableHead>Model / Target</TableHead>
                <TableHead>Latency</TableHead>
                <TableHead>Cost</TableHead>
                <TableHead>Risk Score</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {events.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} className="text-center py-8 text-muted-foreground">
                    Waiting for telemetry events...
                  </TableCell>
                </TableRow>
              ) : (
                events.map((evt) => (
                  <TableRow key={evt.id} className="border-neutral-800 group hover:bg-neutral-900/50 transition-colors">
                    <TableCell className="font-mono text-sm">{evt.time}</TableCell>
                    <TableCell>
                      <Link href={`/traces/${evt.trace_id}`} className="text-blue-400 hover:text-blue-300 font-mono text-sm hover:underline">
                        {evt.trace_id}
                      </Link>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="border-neutral-700 bg-black/50 text-neutral-300">
                        {evt.event_type}
                      </Badge>
                    </TableCell>
                    <TableCell>{evt.model}</TableCell>
                    <TableCell>{evt.latency}ms</TableCell>
                    <TableCell className="text-green-400 font-mono">${evt.cost.toFixed(4)}</TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <div className={`h-2 w-2 rounded-full ${getRiskColor(evt.risk_score)}`} />
                        <span className="font-mono">{evt.risk_score}/100</span>
                      </div>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
