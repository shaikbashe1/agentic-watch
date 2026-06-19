"use client"

import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip } from "recharts"

const mockTimelineEvents = [
  { name: "Agent Start", start: 0, duration: 5, fill: "#4ade80" },
  { name: "LLM Call: gpt-4o", start: 5, duration: 1200, fill: "#3b82f6" },
  { name: "Policy Check", start: 1205, duration: 15, fill: "#8b5cf6" },
  { name: "Tool: search_web", start: 1220, duration: 400, fill: "#f59e0b" },
  { name: "LLM Call: gpt-4o", start: 1620, duration: 800, fill: "#3b82f6" },
  { name: "Agent End", start: 2420, duration: 5, fill: "#4ade80" },
].map(evt => ({ ...evt, end: evt.start + evt.duration })) // Recharts range bar needs [start, end]

export default function SessionTimeline() {
  const { id } = useParams()

  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Session Timeline: {id}</h1>
        <p className="text-muted-foreground">Horizontal flame graph of all operations in this session.</p>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Execution Flame Graph</CardTitle>
          <CardDescription>Visualizing spans and latency (ms).</CardDescription>
        </CardHeader>
        <CardContent className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              layout="vertical"
              data={mockTimelineEvents}
              margin={{ top: 20, right: 20, bottom: 20, left: 100 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={true} vertical={true} />
              <XAxis type="number" stroke="#888" tickFormatter={(val) => `${val}ms`} />
              <YAxis type="category" dataKey="name" stroke="#888" width={120} />
              <RechartsTooltip 
                contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }}
                formatter={(val, name, props) => {
                  return [`${props.payload.duration}ms`, "Duration"]
                }}
              />
              <Bar dataKey={(entry) => [entry.start, entry.end]} fill="#3b82f6" radius={4}>
                {/* We map the fill directly from the data above via custom cell, but Recharts handles array data natively for range bars */}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
