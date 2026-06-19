"use client"

import { useEffect, useState } from "react"
import { useParams } from "next/navigation"
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  Node,
  Edge
} from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { Card } from "@/components/ui/card"

export default function TraceDetail() {
  const { id } = useParams()
  const [nodes, setNodes, onNodesChange] = useNodesState([])
  const [edges, setEdges, onEdgesChange] = useEdgesState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // In production, fetch from /api/v1/analytics/traces/[id]
    // Here we generate mock DAG for the trace
    const mockNodes: Node[] = [
      {
        id: "1",
        position: { x: 250, y: 0 },
        data: { label: "Agent Start: support-bot" },
        style: { background: "#4ade80", color: "#fff", border: "1px solid #22c55e", borderRadius: "8px", padding: "10px" }
      },
      {
        id: "2",
        position: { x: 250, y: 100 },
        data: { label: "LLM Call: gpt-4o" },
        style: { background: "#3b82f6", color: "#fff", border: "1px solid #2563eb", borderRadius: "8px", padding: "10px" }
      },
      {
        id: "3",
        position: { x: 100, y: 200 },
        data: { label: "Tool Call: query_database" },
        style: { background: "#f59e0b", color: "#fff", border: "1px solid #d97706", borderRadius: "8px", padding: "10px" }
      },
      {
        id: "4",
        position: { x: 400, y: 200 },
        data: { label: "Policy Check: ALLOW" },
        style: { background: "#8b5cf6", color: "#fff", border: "1px solid #7c3aed", borderRadius: "8px", padding: "10px" }
      },
      {
        id: "5",
        position: { x: 250, y: 300 },
        data: { label: "Agent End" },
        style: { background: "#4ade80", color: "#fff", border: "1px solid #22c55e", borderRadius: "8px", padding: "10px" }
      }
    ]

    const mockEdges: Edge[] = [
      { id: "e1-2", source: "1", target: "2" },
      { id: "e2-3", source: "2", target: "3", animated: true },
      { id: "e2-4", source: "2", target: "4" },
      { id: "e3-5", source: "3", target: "5" },
      { id: "e4-5", source: "4", target: "5" }
    ]

    setNodes(mockNodes)
    setEdges(mockEdges)
    setLoading(false)
  }, [id, setNodes, setEdges])

  if (loading) {
    return <div className="p-8">Loading execution graph...</div>
  }

  return (
    <div className="p-8 h-[calc(100vh-64px)] flex flex-col">
      <h1 className="text-3xl font-bold mb-2">Trace: {id}</h1>
      <p className="text-muted-foreground mb-4">Execution Graph Analysis</p>
      
      <Card className="flex-1 w-full relative border-neutral-800 bg-black/40">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          colorMode="dark"
        >
          <Controls />
          <MiniMap nodeStrokeWidth={3} />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </Card>
    </div>
  )
}
