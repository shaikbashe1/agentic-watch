"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ZAxis } from "recharts"

const mockToolsData = [
  { name: "read_database", count: 1500, avgRisk: 10, latency: 150 },
  { name: "execute_sql", count: 800, avgRisk: 45, latency: 300 },
  { name: "delete_user", count: 12, avgRisk: 95, latency: 400 },
  { name: "search_web", count: 5000, avgRisk: 5, latency: 800 },
  { name: "read_file", count: 3200, avgRisk: 15, latency: 50 },
  { name: "write_file", count: 450, avgRisk: 30, latency: 120 },
]

const getRiskColor = (risk: number) => {
  if (risk > 80) return "#ef4444" // red
  if (risk > 40) return "#f59e0b" // orange
  return "#4ade80" // green
}

export default function ToolsAnalytics() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Tool Usage</h1>
        <p className="text-muted-foreground">Scatter plot mapping tool invocation frequency against average risk score.</p>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Tool Execution Matrix</CardTitle>
          <CardDescription>X-Axis: Invocation Count | Y-Axis: Average Risk Score | Bubble Size: Latency</CardDescription>
        </CardHeader>
        <CardContent className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" />
              <XAxis type="number" dataKey="count" name="Invocations" stroke="#888" />
              <YAxis type="number" dataKey="avgRisk" name="Risk Score" stroke="#888" domain={[0, 100]} />
              <ZAxis type="number" dataKey="latency" range={[50, 400]} name="Latency" />
              <Tooltip 
                cursor={{ strokeDasharray: '3 3' }} 
                contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }}
                formatter={(value, name, props) => {
                  if (name === "Risk Score") return [`${value}/100`, name]
                  if (name === "Latency") return [`${value}ms`, name]
                  return [value, name]
                }}
              />
              <Scatter name="Tools" data={mockToolsData}>
                {mockToolsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getRiskColor(entry.avgRisk)} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
