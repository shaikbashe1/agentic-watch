"use client"

import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Plus, Settings2 } from "lucide-react"

const mockPolicies = [
  { id: "pol_1", name: "Block destructive commands", action: "BLOCK", conditions: 1, active: true },
  { id: "pol_2", name: "Warn on expensive models in dev", action: "WARN", conditions: 2, active: true },
  { id: "pol_3", name: "Block high risk score", action: "BLOCK", conditions: 1, active: true },
  { id: "pol_4", name: "Redact PII in user prompts", action: "REDACT", conditions: 1, active: false },
]

export default function PolicyManager() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Policy Manager</h1>
          <p className="text-muted-foreground">Govern agent actions before they execute.</p>
        </div>
        <Button asChild className="bg-blue-600 hover:bg-blue-700 text-white">
          <Link href="/policies/new">
            <Plus className="h-4 w-4 mr-2" /> Create Policy
          </Link>
        </Button>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Active Policies</CardTitle>
          <CardDescription>Policies are evaluated in top-down priority order.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Status</TableHead>
                <TableHead>Policy Name</TableHead>
                <TableHead>Action</TableHead>
                <TableHead>Conditions</TableHead>
                <TableHead className="text-right">Manage</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockPolicies.map((pol) => (
                <TableRow key={pol.id} className="border-neutral-800 group hover:bg-neutral-900/50 transition-colors">
                  <TableCell>
                    <Badge variant={pol.active ? "default" : "secondary"} className={pol.active ? "bg-green-500/20 text-green-400" : ""}>
                      {pol.active ? "Enabled" : "Disabled"}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-semibold">{pol.name}</TableCell>
                  <TableCell>
                    <span className={`font-mono text-xs px-2 py-1 rounded-md ${
                      pol.action === "BLOCK" ? "bg-red-500/20 text-red-400" :
                      pol.action === "WARN" ? "bg-yellow-500/20 text-yellow-400" :
                      "bg-blue-500/20 text-blue-400"
                    }`}>
                      {pol.action}
                    </span>
                  </TableCell>
                  <TableCell>{pol.conditions} rule(s)</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="icon">
                      <Settings2 className="h-4 w-4 text-muted-foreground" />
                    </Button>
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
