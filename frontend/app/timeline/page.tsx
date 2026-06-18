"use client";
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function TimelinePage() {
    const [events, setEvents] = useState([]);
    
    useEffect(() => {
        // Fetch timeline events or connect to WS
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/timeline/default_agent`)
            .then(res => res.json())
            .then(data => setEvents(data))
            .catch(console.error);
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Execution Timeline</h1>
            <div className="bg-white p-4 rounded-lg shadow h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={events}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="timestamp" />
                        <YAxis />
                        <Tooltip />
                        <Legend />
                        <Line type="stepAfter" dataKey="duration_ms" stroke="#8884d8" name="Duration (ms)" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            <div className="mt-6 space-y-4">
                {events.map((ev: any, i: number) => (
                    <div key={i} className="p-4 bg-white shadow rounded border-l-4 border-purple-500">
                        <div className="flex justify-between">
                            <strong>{ev.step_type}</strong>
                            <span className="text-gray-500">{new Date(ev.timestamp).toLocaleString()}</span>
                        </div>
                        <div className="text-sm text-gray-600 mt-2">
                            Status: {ev.status} | Duration: {ev.duration_ms}ms
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
