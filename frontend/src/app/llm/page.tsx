export default function LLMDashboard() {
  return (
    <div className="p-8 text-white min-h-screen">
      <h1 className="text-3xl font-bold mb-4">LLM Observability</h1>
      <p>Analyze token usage, prompts, and model distributions across OpenAI, Anthropic, Gemini, etc.</p>
      <div className="grid grid-cols-2 gap-4 mt-8">
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Total Tokens (24h): 1.2M</div>
        <div className="p-4 border border-zinc-800 rounded bg-zinc-900/50">Primary Model: claude-3-sonnet</div>
      </div>
    </div>
  );
}
