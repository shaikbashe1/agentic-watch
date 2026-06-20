import React from 'react';

export default function TracesDashboard() {
  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6 text-blue-400">AgentWatch Telemetry</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-2">Total Workflows</h2>
          <p className="text-4xl font-mono text-green-400">1,248</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-2">Total Agents Executed</h2>
          <p className="text-4xl font-mono text-purple-400">4,192</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700">
          <h2 className="text-xl font-semibold mb-2">LLM Cost (USD)</h2>
          <p className="text-4xl font-mono text-yellow-400">$842.15</p>
        </div>
      </div>

      <h2 className="text-2xl font-semibold mb-4">Recent Traces</h2>
      <div className="bg-gray-800 rounded-lg shadow-lg border border-gray-700 overflow-hidden">
        <table className="w-full text-left">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-4 font-semibold text-gray-300">Trace ID</th>
              <th className="p-4 font-semibold text-gray-300">Workflow Name</th>
              <th className="p-4 font-semibold text-gray-300">Status</th>
              <th className="p-4 font-semibold text-gray-300">Latency</th>
              <th className="p-4 font-semibold text-gray-300">Cost</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-700">
            <tr className="hover:bg-gray-750 transition-colors">
              <td className="p-4 font-mono text-sm text-gray-400">0xc3db1531...</td>
              <td className="p-4">ContentGenerationWorkflow</td>
              <td className="p-4"><span className="px-2 py-1 bg-green-900 text-green-300 rounded text-xs">OK</span></td>
              <td className="p-4">1.2s</td>
              <td className="p-4">$0.04</td>
            </tr>
            <tr className="hover:bg-gray-750 transition-colors">
              <td className="p-4 font-mono text-sm text-gray-400">0xa1bf9284...</td>
              <td className="p-4">CustomerSupportAgent</td>
              <td className="p-4"><span className="px-2 py-1 bg-red-900 text-red-300 rounded text-xs">ERROR</span></td>
              <td className="p-4">5.4s</td>
              <td className="p-4">$0.12</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
