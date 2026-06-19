"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Plus, Trash2, Save } from "lucide-react"

interface Condition {
  field: string
  operator: string
  value: string
}

export default function PolicyBuilder() {
  const router = useRouter()
  const [name, setName] = useState("")
  const [action, setAction] = useState("BLOCK")
  const [conditions, setConditions] = useState<Condition[]>([
    { field: "tool.name", operator: "contains", value: "" }
  ])

  const addCondition = () => {
    setConditions([...conditions, { field: "risk_score", operator: "gt", value: "" }])
  }

  const removeCondition = (index: number) => {
    const newConds = [...conditions]
    newConds.splice(index, 1)
    setConditions(newConds)
  }

  const updateCondition = (index: number, key: keyof Condition, val: string) => {
    const newConds = [...conditions]
    newConds[index][key] = val
    setConditions(newConds)
  }

  const savePolicy = () => {
    // In production, POST to /api/v1/policies
    console.log("Saving policy:", { name, action, conditions })
    router.push("/policies")
  }

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Policy Builder</h1>
          <p className="text-muted-foreground">Create rules to govern agent behavior.</p>
        </div>
      </div>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Rule Details</CardTitle>
          <CardDescription>Name and define the outcome of this rule.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Policy Name</Label>
            <Input id="name" placeholder="e.g. Block destructive commands" value={name} onChange={(e) => setName(e.target.value)} className="bg-black/50 border-neutral-800" />
          </div>
          <div className="space-y-2">
            <Label>Action to Take</Label>
            <Select value={action} onValueChange={setAction}>
              <SelectTrigger className="w-full bg-black/50 border-neutral-800">
                <SelectValue placeholder="Select action" />
              </SelectTrigger>
              <SelectContent className="bg-neutral-900 border-neutral-800">
                <SelectItem value="ALLOW" className="text-green-500">Allow</SelectItem>
                <SelectItem value="WARN" className="text-yellow-500">Warn</SelectItem>
                <SelectItem value="BLOCK" className="text-red-500">Block</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      <Card className="border-neutral-800 bg-black/40">
        <CardHeader>
          <CardTitle>Conditions</CardTitle>
          <CardDescription>If ALL of these conditions match, the action will be triggered.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {conditions.map((cond, idx) => (
            <div key={idx} className="flex items-center gap-4 p-4 rounded-md border border-neutral-800 bg-black/50">
              <div className="flex-1">
                <Select value={cond.field} onValueChange={(val) => updateCondition(idx, "field", val)}>
                  <SelectTrigger className="bg-black/50 border-neutral-800">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-neutral-900 border-neutral-800">
                    <SelectItem value="tool.name">Tool Name</SelectItem>
                    <SelectItem value="llm.model">LLM Model</SelectItem>
                    <SelectItem value="risk_score">Risk Score</SelectItem>
                    <SelectItem value="environment">Environment</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex-1">
                <Select value={cond.operator} onValueChange={(val) => updateCondition(idx, "operator", val)}>
                  <SelectTrigger className="bg-black/50 border-neutral-800">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent className="bg-neutral-900 border-neutral-800">
                    <SelectItem value="eq">Equals (=)</SelectItem>
                    <SelectItem value="contains">Contains</SelectItem>
                    <SelectItem value="gt">Greater Than (&gt;)</SelectItem>
                    <SelectItem value="lt">Less Than (&lt;)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="flex-1">
                <Input 
                  placeholder="Value" 
                  value={cond.value} 
                  onChange={(e) => updateCondition(idx, "value", e.target.value)} 
                  className="bg-black/50 border-neutral-800"
                />
              </div>
              <Button variant="ghost" size="icon" onClick={() => removeCondition(idx)} className="text-red-500 hover:bg-red-500/10">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
          
          <Button variant="outline" onClick={addCondition} className="w-full border-neutral-800 bg-transparent hover:bg-neutral-900 border-dashed">
            <Plus className="h-4 w-4 mr-2" /> Add Condition
          </Button>
        </CardContent>
        <CardFooter className="flex justify-end gap-2 border-t border-neutral-800 pt-6">
          <Button variant="ghost" onClick={() => router.push("/policies")}>Cancel</Button>
          <Button onClick={savePolicy} className="bg-blue-600 hover:bg-blue-700 text-white">
            <Save className="h-4 w-4 mr-2" /> Save Policy
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
