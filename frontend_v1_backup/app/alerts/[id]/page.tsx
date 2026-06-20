"use client"

import { useParams } from "next/navigation"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { AlertTriangle, CheckCircle } from "lucide-react"

export default function AlertDetail() {
  const { id } = useParams()

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">Incident Detail: {id}</h1>
            <Badge variant="destructive" className="bg-red-500">HIGH SEVERITY</Badge>
          </div>
          <p className="text-muted-foreground mt-2">Fired on 2026-06-19 14:15:00</p>
        </div>
        <Button className="bg-green-600 hover:bg-green-700 text-white">
          <CheckCircle className="h-4 w-4 mr-2" /> Mark as Resolved
        </Button>
      </div>

      <Card className="border-neutral-800 bg-black/40 border-l-4 border-l-red-500">
        <CardHeader>
          <CardTitle className="text-red-400 flex items-center gap-2">
            <AlertTriangle className="h-5 w-5" /> High Cost Spike Detected
          </CardTitle>
          <CardDescription>This alert was triggered by rule: "High Cost Spike"</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 bg-neutral-900/50 p-4 rounded-md">
            <div>
              <p className="text-sm text-muted-foreground">Metric Monitored</p>
              <p className="font-semibold font-mono">Cost / Hour</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Threshold Value</p>
              <p className="font-semibold font-mono">{`> $50`}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Actual Value</p>
              <p className="font-semibold font-mono text-red-400">$84.50</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Affected Workspace</p>
              <p className="font-semibold font-mono">ws_acme_corp</p>
            </div>
          </div>
          
          <div>
            <h3 className="font-bold text-lg mb-2">Root Cause Analysis</h3>
            <p className="text-sm text-muted-foreground">
              Agent `Data Analysis Agent (v1.0.5)` initiated 45 consecutive calls to `gpt-4o` resulting in 8.5 million input tokens processed within 15 minutes. 
              The agent was caught in a recursive extraction loop parsing a 400MB dataset.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
