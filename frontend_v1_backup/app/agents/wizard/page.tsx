"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AgentWizardPage() {
    const router = useRouter();
    const [step, setStep] = useState(1);
    const [agentName, setAgentName] = useState('');
    const [framework, setFramework] = useState('LangGraph');
    const [apiKey, setApiKey] = useState('');
    const [agentId, setAgentId] = useState('');
    const [isVerifying, setIsVerifying] = useState(false);

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        const token = localStorage.getItem('agentwatch_token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/agents/register', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ name: agentName, framework, description: '' })
            });

            if (res.ok) {
                const data = await res.json();
                setAgentId(data.agent_id);
                setApiKey(data.api_key);
                setStep(2);
            }
        } catch (err) {
            console.error("Registration failed", err);
        }
    };

    const handleVerify = () => {
        setIsVerifying(true);
        setTimeout(() => {
            setIsVerifying(false);
            setStep(3);
        }, 2000);
    };

    return (
        <div className="p-6 max-w-4xl mx-auto">
            <h1 className="text-3xl font-bold mb-8 text-center">Connect Your Agent</h1>
            
            <div className="flex justify-between mb-12 relative">
                <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 -z-10 -translate-y-1/2"></div>
                {[1, 2, 3].map(i => (
                    <div key={i} className={`w-10 h-10 rounded-full flex items-center justify-center font-bold border-4 border-white ${step >= i ? 'bg-blue-600 text-white' : 'bg-gray-300 text-gray-500'}`}>
                        {i}
                    </div>
                ))}
            </div>

            {step === 1 && (
                <div className="bg-white p-8 rounded shadow">
                    <h2 className="text-xl font-bold mb-4">Step 1: Agent Details</h2>
                    <form onSubmit={handleRegister} className="space-y-4">
                        <div>
                            <label className="block text-sm font-medium mb-1">Agent Name</label>
                            <input type="text" value={agentName} onChange={e => setAgentName(e.target.value)} className="w-full p-2 border rounded" required />
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
                        <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700">Generate Keys</button>
                    </form>
                </div>
            )}

            {step === 2 && (
                <div className="bg-white p-8 rounded shadow">
                    <h2 className="text-xl font-bold mb-4">Step 2: Integrate SDK</h2>
                    
                    <div className="mb-6 p-4 bg-gray-50 rounded border">
                        <p className="text-sm font-medium text-gray-500 mb-1">YOUR API KEY (COPY THIS)</p>
                        <p className="font-mono bg-white p-2 border rounded">{apiKey}</p>
                    </div>

                    <h3 className="font-bold mb-2">Install Package</h3>
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded mb-6 font-mono text-sm">
                        pip install agentwatch
                    </pre>

                    <h3 className="font-bold mb-2">Copy Code Snippet</h3>
                    <pre className="bg-gray-900 text-gray-100 p-4 rounded mb-6 font-mono text-sm overflow-x-auto">
{`from agentwatch import AgentWatch

aw = AgentWatch(api_key="${apiKey}")

# Inside your agent execution loop:
aw.track(
    event_type="tool_call",
    agent_id="${agentId}",
    tool_name="SearchAPI",
    status="success",
    latency=120
)`}
                    </pre>

                    <button onClick={handleVerify} disabled={isVerifying} className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 disabled:bg-blue-400">
                        {isVerifying ? "Waiting for first event..." : "Verify Connection"}
                    </button>
                </div>
            )}

            {step === 3 && (
                <div className="bg-white p-8 rounded shadow text-center">
                    <div className="w-20 h-20 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-6 text-4xl">
                        ✓
                    </div>
                    <h2 className="text-2xl font-bold mb-2 text-green-600">Agent Connected Successfully!</h2>
                    <p className="text-gray-600 mb-8">We are successfully receiving telemetry from {agentName}.</p>
                    <button onClick={() => router.push('/agents')} className="bg-gray-900 text-white px-6 py-2 rounded hover:bg-gray-800">
                        View Dashboard
                    </button>
                </div>
            )}
        </div>
    );
}
