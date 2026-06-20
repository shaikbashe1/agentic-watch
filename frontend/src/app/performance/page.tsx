export default function PerformanceDashboard() {
  return (
    <div className="p-8 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Agent Performance</h1>
      <p>Analyze latency, retries, and task success rates.</p>
      {/* Mockup panels would go here */}
      <div className="grid grid-cols-2 gap-4 mt-8">
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Task Success Rate: 98.4%</div>
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Avg Workflow Latency: 2.1s</div>
      </div>
    </div>
  );
}
