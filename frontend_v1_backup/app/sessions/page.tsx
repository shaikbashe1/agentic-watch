"use client"

import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Play } from "lucide-react"

const mockSessions = [
  { id: "sess_xyz123", agent: "Customer Support Bot", version: "2.1.0", start: "2026-06-19 14:00:21", events: 14, risk: 20 },
  { id: "sess_abc987", agent: "Data Analysis Agent", version: "1.0.5", start: "2026-06-19 13:45:11", events: 42, risk: 85 },
  { id: "sess_qwerty", agent: "Code Reviewer", version: "3.2.1", start: "2026-06-19 12:30:00", events: 5, risk: 10 },
]

export default function SessionsList() {
  return (
    <div className="p-8 max-w-6xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Agent Sessions</h1>
          <p className="text-muted-foreground">Historical list of distinct agent run sessions.</p>
        </div>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Recent Sessions</CardTitle>
          <CardDescription>Click a session ID to view its execution timeline.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>Session ID</TableHead>
                <TableHead>Agent Name</TableHead>
                <TableHead>Version</TableHead>
                <TableHead>Start Time</TableHead>
                <TableHead>Events</TableHead>
                <TableHead>Max Risk</TableHead>
                <TableHead>Action</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockSessions.map((sess) => (
                <TableRow key={sess.id} className="border-neutral-800 group hover:bg-neutral-900/50 transition-colors">
                  <TableCell>
                    <Link href={`/sessions/${sess.id}`} className="text-blue-400 font-mono text-sm hover:underline">
                      {sess.id}
                    </Link>
                  </TableCell>
                  <TableCell className="font-semibold">{sess.agent}</TableCell>
                  <TableCell>
                    <Badge variant="outline" className="border-neutral-700 bg-black/50 text-neutral-300">
                      v{sess.version}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-mono text-sm">{sess.start}</TableCell>
                  <TableCell>{sess.events}</TableCell>
                  <TableCell>
                    <span className={sess.risk > 80 ? "text-red-500 font-bold" : sess.risk > 40 ? "text-yellow-500" : "text-green-500"}>
                      {sess.risk}/100
                    </span>
                  </TableCell>
                  <TableCell>
                    <Link href={`/sessions/${sess.id}`}>
                      <Play className="h-4 w-4 text-blue-500 hover:text-blue-400 cursor-pointer" />
                    </Link>
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
