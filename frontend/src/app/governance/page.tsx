export default function GovernanceDashboard() {
  return (
    <div className="p-8 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Governance & Security</h1>
      <p>Monitor PII violations, Prompt Injections, and RAGAS Hallucination scores.</p>
      <div className="grid grid-cols-2 gap-4 mt-8">
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Blocked Injections: 12</div>
        <div className="p-4 border border-red-900/50 rounded bg-red-900/20 text-red-400">PII Leaks Prevented: 3</div>
      </div>
    </div>
  );
}
