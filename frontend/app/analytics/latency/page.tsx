"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, AreaChart, Area } from "recharts"

const mockData = [
  { time: "00:00", p50: 120, p95: 450, p99: 800 },
  { time: "04:00", p50: 130, p95: 480, p99: 850 },
  { time: "08:00", p50: 200, p95: 700, p99: 1200 },
  { time: "12:00", p50: 250, p95: 850, p99: 1500 },
  { time: "16:00", p50: 220, p95: 750, p99: 1300 },
  { time: "20:00", p50: 150, p95: 500, p99: 900 },
]

export default function LatencyAnalytics() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Latency Analysis</h1>
        <p className="text-muted-foreground">Monitor P50, P95, and P99 API response times across your agents.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="border-neutral-800 bg-black/40">
          <CardHeader>
            <CardTitle>Latency Trends</CardTitle>
            <CardDescription>Response time percentiles over the last 24 hours.</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="time" stroke="#888" />
                <YAxis stroke="#888" tickFormatter={(v) => `${v}ms`} />
                <Tooltip contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }} />
                <Legend />
                <Line type="monotone" dataKey="p50" stroke="#4ade80" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="p95" stroke="#f59e0b" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="p99" stroke="#ef4444" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="border-neutral-800 bg-black/40">
          <CardHeader>
            <CardTitle>Latency Distribution</CardTitle>
            <CardDescription>Area curve showing the density of high-latency requests.</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="time" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }} />
                <Area type="monotone" dataKey="p99" stackId="1" stroke="#ef4444" fill="#ef4444" fillOpacity={0.2} />
                <Area type="monotone" dataKey="p95" stackId="2" stroke="#f59e0b" fill="#f59e0b" fillOpacity={0.2} />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
