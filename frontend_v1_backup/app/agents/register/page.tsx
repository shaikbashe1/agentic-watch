"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterAgentPage() {
    const router = useRouter();
    const [name, setName] = useState('');
    const [framework, setFramework] = useState('LangGraph');
    const [description, setDescription] = useState('');

    const handleRegister = (e: React.FormEvent) => {
        e.preventDefault();
        // Call API
        router.push('/agents');
    };

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Register New Agent</h1>
            <div className="bg-white p-6 rounded shadow max-w-lg">
                <form onSubmit={handleRegister} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">Agent Name</label>
                        <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full p-2 border rounded" placeholder="e.g. CustomerSupportBot" required />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Framework</label>
                        <select value={framework} onChange={e => setFramework(e.target.value)} className="w-full p-2 border rounded">
                            <option>LangGraph</option>
                            <option>CrewAI</option>
                            <option>AutoGen</option>
                            <option>OpenAI Swarm</option>
                            <option>Custom</option>
                        </select>
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Description</label>
                        <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full p-2 border rounded" rows={3}></textarea>
                    </div>
                    <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Register Agent</button>
                </form>
            </div>
        </div>
    );
}
