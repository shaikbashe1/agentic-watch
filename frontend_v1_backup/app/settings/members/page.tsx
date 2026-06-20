"use client"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { UserPlus, Shield } from "lucide-react"

const mockMembers = [
  { id: "usr_9fa29", email: "admin@acmecorp.com", role: "Owner", joined: "2024-01-15" },
  { id: "usr_8fa28", email: "security@acmecorp.com", role: "Admin", joined: "2024-02-20" },
  { id: "usr_7fa27", email: "dev-lead@acmecorp.com", role: "Developer", joined: "2024-03-10" },
  { id: "usr_6fa26", email: "auditor@external.com", role: "Viewer", joined: "2024-05-01" },
]

export default function TeamManagement() {
  return (
    <div className="p-8 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">Team Management</h1>
          <p className="text-muted-foreground mt-2">Manage workspace members and their RBAC roles.</p>
        </div>
        <Button className="bg-blue-600 hover:bg-blue-700 text-white">
          <UserPlus className="h-4 w-4 mr-2" /> Invite Member
        </Button>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Shield className="h-5 w-5" /> Workspace Members
          </CardTitle>
          <CardDescription>All users with access to the `ws_acme_corp` workspace.</CardDescription>
        </CardHeader>
        <CardContent className="p-0">
          <Table>
            <TableHeader className="bg-neutral-900/50">
              <TableRow className="border-neutral-800">
                <TableHead>User ID</TableHead>
                <TableHead>Email</TableHead>
                <TableHead>Role</TableHead>
                <TableHead>Joined At</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {mockMembers.map((member) => (
                <TableRow key={member.id} className="border-neutral-800">
                  <TableCell className="font-mono text-sm text-neutral-400">{member.id}</TableCell>
                  <TableCell className="font-semibold">{member.email}</TableCell>
                  <TableCell>
                    <Badge 
                      variant="outline" 
                      className={
                        member.role === "Owner" ? "border-purple-500 text-purple-400" :
                        member.role === "Admin" ? "border-red-500 text-red-400" :
                        member.role === "Developer" ? "border-blue-500 text-blue-400" :
                        "border-neutral-500 text-neutral-400"
                      }
                    >
                      {member.role}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-muted-foreground">{member.joined}</TableCell>
                  <TableCell className="text-right">
                    <Button variant="ghost" size="sm" className="text-neutral-400 hover:text-white">Edit Role</Button>
                    <Button variant="ghost" size="sm" className="text-red-400 hover:text-red-300">Remove</Button>
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
