"use client";
import React, { useEffect, useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function CostsPage() {
    const [metrics, setMetrics] = useState([]);
    
    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/metrics/tokens`)
            .then(res => res.json())
            .then(data => setMetrics(data))
            .catch(console.error);
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Token & Cost Monitoring</h1>
            <div className="bg-white p-4 rounded-lg shadow h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={metrics}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="timestamp" />
                        <YAxis />
                        <Tooltip />
                        <Area type="monotone" dataKey="total_tokens" stroke="#10b981" fill="#10b981" fillOpacity={0.3} name="Total Tokens" />
                        <Area type="monotone" dataKey="cost_usd" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} name="Cost ($)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
