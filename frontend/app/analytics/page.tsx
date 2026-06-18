"use client";
import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function AnalyticsPage() {
    const [metrics, setMetrics] = useState([]);
    
    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/tool-traces`)
            .then(res => res.json())
            .then(data => {
                // Group by tool_name
                const tools: any = {};
                data.forEach((trace: any) => {
                    if (!tools[trace.tool_name]) {
                        tools[trace.tool_name] = { tool_name: trace.tool_name, success: 0, failure: 0, avgLatency: 0, count: 0 };
                    }
                    if (trace.success) tools[trace.tool_name].success += 1;
                    else tools[trace.tool_name].failure += 1;
                    
                    tools[trace.tool_name].avgLatency += trace.latency_ms;
                    tools[trace.tool_name].count += 1;
                });

                Object.values(tools).forEach((t: any) => {
                    t.avgLatency = t.avgLatency / t.count;
                });

                setMetrics(Object.values(tools));
            })
            .catch(console.error);
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Agent Performance Analytics</h1>
            <div className="bg-white p-4 rounded-lg shadow h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="tool_name" />
                        <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
                        <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
                        <Tooltip />
                        <Legend />
                        <Bar yAxisId="left" dataKey="success" stackId="a" fill="#10b981" name="Successful Uses" />
                        <Bar yAxisId="left" dataKey="failure" stackId="a" fill="#ef4444" name="Failed Uses" />
                        <Bar yAxisId="right" dataKey="avgLatency" fill="#8884d8" name="Avg Latency (ms)" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
