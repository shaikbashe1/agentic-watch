"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, PieChart, Pie, Cell } from "recharts"

const mockCostOverTime = [
  { date: "Mon", "gpt-4o": 12.5, "claude-3-5": 8.2, "gemini-1.5": 3.1 },
  { date: "Tue", "gpt-4o": 15.0, "claude-3-5": 9.5, "gemini-1.5": 4.0 },
  { date: "Wed", "gpt-4o": 18.2, "claude-3-5": 11.1, "gemini-1.5": 5.2 },
  { date: "Thu", "gpt-4o": 22.4, "claude-3-5": 14.5, "gemini-1.5": 7.8 },
  { date: "Fri", "gpt-4o": 25.1, "claude-3-5": 16.0, "gemini-1.5": 8.5 },
  { date: "Sat", "gpt-4o": 10.5, "claude-3-5": 5.2, "gemini-1.5": 2.1 },
  { date: "Sun", "gpt-4o": 8.4, "claude-3-5": 4.1, "gemini-1.5": 1.5 },
]

const mockModelDistribution = [
  { name: "gpt-4o", value: 112.1 },
  { name: "claude-3-5-sonnet", value: 68.6 },
  { name: "gemini-1.5-pro", value: 32.2 },
  { name: "gpt-4o-mini", value: 12.4 },
]

const COLORS = ["#3b82f6", "#f59e0b", "#4ade80", "#a855f7"]

export default function CostAnalytics() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Cost Breakdown</h1>
        <p className="text-muted-foreground">Monitor exact USD token spend across all agents and LLM providers.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="border-neutral-800 bg-black/40 lg:col-span-2">
          <CardHeader>
            <CardTitle>Daily Spend by Model</CardTitle>
            <CardDescription>Stacked bar chart showing API costs over the last 7 days.</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockCostOverTime}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                <XAxis dataKey="date" stroke="#888" />
                <YAxis stroke="#888" tickFormatter={(v) => `$${v}`} />
                <RechartsTooltip contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }} formatter={(val) => `$${Number(val).toFixed(2)}`} />
                <Legend />
                <Bar dataKey="gpt-4o" stackId="a" fill="#3b82f6" />
                <Bar dataKey="claude-3-5" stackId="a" fill="#f59e0b" />
                <Bar dataKey="gemini-1.5" stackId="a" fill="#4ade80" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="border-neutral-800 bg-black/40">
          <CardHeader>
            <CardTitle>Total Spend Distribution</CardTitle>
            <CardDescription>Proportional cost per model.</CardDescription>
          </CardHeader>
          <CardContent className="h-[400px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={mockModelDistribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent = 0 }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                >
                  {mockModelDistribution.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: "#1a1a1a", borderColor: "#333" }} formatter={(val) => `$${Number(val).toFixed(2)}`} />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
