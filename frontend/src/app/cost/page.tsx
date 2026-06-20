export default function CostDashboard() {
  return (
    <div className="p-8 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Cost Intelligence</h1>
      <p>Monitor USD spend per workflow, agent, and LLM model.</p>
      <div className="grid grid-cols-2 gap-4 mt-8">
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Daily Spend: $42.50</div>
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Most Expensive Agent: Researcher</div>
      </div>
    </div>
  );
}
