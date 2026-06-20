"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function APIKeysPage() {
    const router = useRouter();
    const [keys, setKeys] = useState<any[]>([]);

    useEffect(() => {
        fetchKeys();
    }, []);

    const fetchKeys = async () => {
        const token = localStorage.getItem('agentwatch_token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/api-keys', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setKeys(data);
            }
        } catch (err) {
            console.error("Failed to fetch API keys", err);
        }
    };

    const handleRevoke = async (keyId: string) => {
        const token = localStorage.getItem('agentwatch_token');
        if (!token) return;

        try {
            const res = await fetch(`http://localhost:8000/api-keys/${keyId}`, {
                method: 'DELETE',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                fetchKeys();
            }
        } catch (err) {
            console.error("Failed to revoke API key", err);
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">API Keys</h1>
            <p className="mb-6 text-gray-600">Manage the API keys used by your agents to authenticate with the Agentic Watch telemetry ingestion API.</p>
            
            <button onClick={() => router.push('/agents/wizard')} className="bg-blue-600 text-white px-4 py-2 rounded mb-6 hover:bg-blue-700">Generate New Key</button>

            <div className="bg-white rounded shadow">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-gray-50 border-b">
                            <th className="p-4 font-medium text-gray-600">Key Name</th>
                            <th className="p-4 font-medium text-gray-600">API Key</th>
                            <th className="p-4 font-medium text-gray-600">Status</th>
                            <th className="p-4 font-medium text-gray-600">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {keys.map(k => (
                            <tr key={k.id} className="border-b last:border-0 hover:bg-gray-50">
                                <td className="p-4">{k.name}</td>
                                <td className="p-4 font-mono text-sm">{k.key}</td>
                                <td className="p-4">
                                    {k.active ? (
                                        <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">Active</span>
                                    ) : (
                                        <span className="bg-red-100 text-red-800 px-2 py-1 rounded text-xs">Revoked</span>
                                    )}
                                </td>
                                <td className="p-4">
                                    {k.active && (
                                        <button onClick={() => handleRevoke(k.id)} className="text-red-600 hover:underline text-sm">Revoke</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {keys.length === 0 && <div className="p-8 text-center text-gray-500">No API keys found. Register an agent to generate one.</div>}
            </div>
        </div>
    );
}
