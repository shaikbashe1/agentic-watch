"use client";

import React, { useEffect, useState, useMemo, useCallback } from "react";
import { useParams } from "next/navigation";
import { useTrace } from "@/hooks/useApi";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType,
  Handle,
  Position,
  Node,
  Edge
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import dagre from "dagre";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

// Custom Node for Trace Events
const TraceNode = ({ data }: { data: any }) => {
  return (
    <div className={`px-4 py-2 shadow-md rounded-md border-2 bg-card ${data.risk_score >= 80 ? 'border-red-500 shadow-red-500/20' : 'border-border'}`}>
      <Handle type="target" position={Position.Top} className="w-16 !bg-muted-foreground" />
      <div className="flex flex-col">
        <div className="text-xs text-muted-foreground mb-1 uppercase tracking-wider font-semibold">
          {data.event_type}
        </div>
        <div className="font-bold text-sm truncate max-w-[200px]" title={data.action}>
          {data.action || data.tool_name || data.llm_model || "Execution"}
        </div>
        <div className="flex gap-2 mt-2">
          {data.latency_ms > 0 && (
            <Badge variant="secondary" className="text-[10px]">{data.latency_ms}ms</Badge>
          )}
          {data.cost_usd > 0 && (
            <Badge variant="outline" className="text-[10px] text-green-500 border-green-500/30">${data.cost_usd.toFixed(4)}</Badge>
          )}
          {data.risk_score >= 80 && (
             <Badge variant="destructive" className="text-[10px]">RISK: {data.risk_score}</Badge>
          )}
        </div>
      </div>
      <Handle type="source" position={Position.Bottom} className="w-16 !bg-muted-foreground" />
    </div>
  );
};

const nodeTypes = {
  traceNode: TraceNode,
};

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const getLayoutedElements = (nodes: any[], edges: any[], direction = 'TB') => {
  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: 250, height: 100 });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  const newNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    const newNode = {
      ...node,
      targetPosition: isHorizontal ? 'left' : 'top',
      sourcePosition: isHorizontal ? 'right' : 'bottom',
      position: {
        x: nodeWithPosition.x - 250 / 2,
        y: nodeWithPosition.y - 100 / 2,
      },
    };
    return newNode;
  });

  return { nodes: newNodes, edges };
};


export default function TraceGraph() {
  const params = useParams();
  const traceId = params?.id as string;
  const { data: traceEvents, isLoading } = useTrace(traceId);

  const [nodes, setNodes, onNodesChange] = useNodesState<Node>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge>([]);

  useEffect(() => {
    if (!traceEvents || traceEvents.length === 0) return;

    const newNodes = traceEvents.map((ev) => ({
      id: ev.span_id,
      type: 'traceNode',
      data: {
        event_type: ev.event_type,
        action: ev.payload?.action || ev.payload?.name || ev.event_type,
        tool_name: ev.tool_name,
        llm_model: ev.llm_model,
        latency_ms: ev.latency_ms,
        cost_usd: ev.cost_usd,
        risk_score: ev.risk_score
      },
      position: { x: 0, y: 0 } // initial position before layout
    }));

    const newEdges = traceEvents
      .filter((ev) => ev.parent_span_id)
      .map((ev) => ({
        id: `e-${ev.parent_span_id}-${ev.span_id}`,
        source: ev.parent_span_id,
        target: ev.span_id,
        type: 'smoothstep',
        animated: true,
        markerEnd: {
          type: MarkerType.ArrowClosed,
          color: '#888',
        },
        style: { stroke: '#888', strokeWidth: 2 }
      }));

    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
      newNodes,
      newEdges
    );

    setNodes(layoutedNodes);
    setEdges(layoutedEdges);

  }, [traceEvents, setNodes, setEdges]);

  if (isLoading) {
    return <div className="p-8">Loading Trace Graph...</div>;
  }

  return (
    <div className="flex flex-col h-[calc(100vh-100px)] space-y-4">
      <div>
        <h1 className="text-2xl font-bold">Execution Trace</h1>
        <p className="text-sm text-muted-foreground font-mono mt-1">{traceId}</p>
      </div>
      <Card className="flex-1 rounded-xl overflow-hidden border-border/50">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-right"
        >
          <MiniMap 
            className="bg-card border border-border" 
            maskColor="rgba(0,0,0,0.2)"
            nodeColor={(n: any) => {
                if (n.data?.risk_score >= 80) return '#ef4444';
                return '#3b82f6';
            }} 
          />
          <Controls className="bg-card text-foreground fill-foreground border-border" />
          <Background color="#555" gap={16} />
        </ReactFlow>
      </Card>
    </div>
  );
}
