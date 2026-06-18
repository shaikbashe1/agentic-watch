"use client";
import React, { useEffect, useState } from 'react';

export default function WorkflowsPage() {
    const [workflows, setWorkflows] = useState([]);
    
    useEffect(() => {
        fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/workflows`)
            .then(res => res.json())
            .then(data => setWorkflows(data))
            .catch(console.error);
    }, []);

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Workflow Executions</h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {workflows.map((wf: any, i: number) => (
                    <div key={i} className="p-4 bg-white shadow rounded border border-gray-200">
                        <div className="flex justify-between items-center mb-4 border-b pb-2">
                            <span className="font-bold text-gray-800">Agent: {wf.agent_id}</span>
                            <span className={`px-2 py-1 rounded text-sm ${wf.status === 'Completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                                {wf.status}
                            </span>
                        </div>
                        <div className="mb-2">
                            <strong>User Request:</strong>
                            <p className="text-gray-600 bg-gray-50 p-2 rounded mt-1">{wf.user_request}</p>
                        </div>
                        <div className="mt-4">
                            <strong>Execution Flow:</strong>
                            <div className="flex flex-wrap gap-2 mt-2">
                                {wf.flow_data ? JSON.parse(wf.flow_data).map((node: string, idx: number) => (
                                    <React.Fragment key={idx}>
                                        <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                                            {node}
                                        </div>
                                        {idx < JSON.parse(wf.flow_data).length - 1 && (
                                            <div className="text-gray-400 mt-1">→</div>
                                        )}
                                    </React.Fragment>
                                )) : <span className="text-gray-400 text-sm">No flow data recorded</span>}
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
