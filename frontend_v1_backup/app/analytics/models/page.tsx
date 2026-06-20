"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts"

const mockModelUsage = [
  { model: "gpt-4o", calls: 45000, errors: 120 },
  { model: "claude-3-5", calls: 32000, errors: 45 },
  { model: "gemini-1.5", calls: 18000, errors: 200 },
  { model: "gpt-4o-mini", calls: 85000, errors: 80 },
  { model: "bedrock-titan", calls: 5000, errors: 10 },
]

export default function ModelsAnalytics() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Model Usage</h1>
        <p className="text-muted-foreground">Analyze API call volume and error rates across different LLMs.</p>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Total API Calls by Model</CardTitle>
          <CardDescription>Bar chart of successful vs failed calls over the last 30 days.</CardDescription>
        </CardHeader>
        <CardContent className="h-[500px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={mockModelUsage} layout="vertical" margin={{ left: 40 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={true} vertical={false} />
              <XAxis type="number" stroke="#888" />
              <YAxis type="category" dataKey="model" stroke="#888" />
              <Tooltip contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }} />
              <Legend />
              <Bar dataKey="calls" name="Successful Calls" fill="#3b82f6" radius={[0, 4, 4, 0]} />
              <Bar dataKey="errors" name="Errors/Failures" fill="#ef4444" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
