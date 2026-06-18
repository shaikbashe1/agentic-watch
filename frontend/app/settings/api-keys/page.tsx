"use client";
import React, { useState } from 'react';

export default function APIKeysPage() {
    const [keys, setKeys] = useState([
        { id: '1', name: 'Production Agent Key', key: 'ak_prod_12345...', active: true },
        { id: '2', name: 'Dev Testing Key', key: 'ak_test_67890...', active: true }
    ]);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">API Keys</h1>
            <p className="mb-6 text-gray-600">Manage the API keys used by your agents to authenticate with the Agentic Watch telemetry ingestion API.</p>
            
            <button className="bg-blue-600 text-white px-4 py-2 rounded mb-6 hover:bg-blue-700">Generate New Key</button>

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
                                    <span className="bg-green-100 text-green-800 px-2 py-1 rounded text-xs">Active</span>
                                </td>
                                <td className="p-4">
                                    <button className="text-red-600 hover:underline text-sm">Revoke</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
