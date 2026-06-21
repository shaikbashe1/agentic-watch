import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-[#050505] text-white font-sans selection:bg-purple-500/30">
      {/* Background gradients */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-purple-900/20 blur-[120px]" />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-blue-900/20 blur-[120px]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-12">
        {/* Header */}
        <header className="flex justify-between items-center mb-16 border-b border-white/10 pb-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-blue-600 flex items-center justify-center shadow-lg shadow-purple-500/20">
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold tracking-tight">Agentic<span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-400">Watch</span></h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-2 text-sm text-zinc-400 bg-white/5 px-4 py-2 rounded-full border border-white/10 backdrop-blur-md">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
              </span>
              System Online
            </span>
          </div>
        </header>

        {/* Metrics Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {[
            { label: 'Active Agents', value: '12', change: '+2', trend: 'up' },
            { label: 'Tasks Processed (24h)', value: '8,439', change: '+14%', trend: 'up' },
            { label: 'System Error Rate', value: '0.04%', change: '-0.01%', trend: 'down' },
          ].map((metric, i) => (
            <div key={i} className="bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md hover:bg-white/10 transition-colors duration-300">
              <p className="text-zinc-400 text-sm font-medium mb-2">{metric.label}</p>
              <div className="flex items-end gap-3">
                <h2 className="text-4xl font-bold text-white">{metric.value}</h2>
                <span className={`text-sm font-medium mb-1 ${metric.trend === 'up' ? 'text-green-400' : 'text-green-400'}`}>
                  {metric.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Active Agents Grid */}
          <div className="lg:col-span-2 space-y-6">
            <h3 className="text-xl font-semibold text-zinc-200 flex items-center gap-2">
              <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
              Active Autonomous Agents
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { name: 'Research-Alpha', role: 'Deep Web Researcher', status: 'Processing', tokens: '45.2k' },
                { name: 'Coder-Bot-X', role: 'Frontend Developer', status: 'Idle', tokens: '12.8k' },
                { name: 'Data-Analyzer-01', role: 'Data Scientist', status: 'Processing', tokens: '89.1k' },
                { name: 'QA-Tester-Prime', role: 'Quality Assurance', status: 'Offline', tokens: '0' },
              ].map((agent, i) => (
                <div key={i} className="group bg-gradient-to-b from-white/5 to-transparent border border-white/10 rounded-2xl p-5 hover:border-purple-500/30 transition-all duration-300">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h4 className="text-lg font-medium text-white group-hover:text-purple-300 transition-colors">{agent.name}</h4>
                      <p className="text-sm text-zinc-400">{agent.role}</p>
                    </div>
                    <div className={`px-2.5 py-1 rounded-full text-xs font-medium border ${
                      agent.status === 'Processing' ? 'bg-blue-500/10 text-blue-400 border-blue-500/20' : 
                      agent.status === 'Idle' ? 'bg-zinc-500/10 text-zinc-400 border-zinc-500/20' : 
                      'bg-red-500/10 text-red-400 border-red-500/20'
                    }`}>
                      {agent.status}
                    </div>
                  </div>
                  <div className="flex items-center gap-2 text-xs text-zinc-500">
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                    {agent.tokens} tokens consumed
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Telemetry Log */}
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-zinc-200 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h8m-8 6h16" />
              </svg>
              Live Telemetry
            </h3>
            <div className="bg-black/50 border border-white/10 rounded-2xl p-4 font-mono text-xs text-zinc-400 h-[340px] overflow-hidden relative">
              <div className="absolute top-0 left-0 w-full h-8 bg-gradient-to-b from-black/80 to-transparent z-10" />
              <div className="absolute bottom-0 left-0 w-full h-8 bg-gradient-to-t from-black/80 to-transparent z-10" />
              <div className="space-y-3 animate-pulse">
                <p><span className="text-blue-400">[17:04:12]</span> [Research-Alpha] Executed Google Search API: "Next.js performance patterns"</p>
                <p><span className="text-blue-400">[17:04:15]</span> [Research-Alpha] Parsed 4,200 tokens from top 3 results.</p>
                <p><span className="text-purple-400">[17:04:18]</span> [Coder-Bot-X] Invoked via IPC from Research-Alpha.</p>
                <p><span className="text-purple-400">[17:04:22]</span> [Coder-Bot-X] Editing frontend/src/app/page.tsx...</p>
                <p><span className="text-green-400">[17:04:25]</span> [System] File saved successfully. HMR triggered.</p>
                <p><span className="text-blue-400">[17:04:28]</span> [Research-Alpha] Idling...</p>
                <p><span className="text-yellow-400">[17:04:30]</span> [Data-Analyzer-01] Warning: High memory usage in Pandas frame.</p>
                <p><span className="text-blue-400">[17:04:31]</span> [Data-Analyzer-01] Garbage collection forced. Mem: 4.2GB -{'>'} 1.1GB.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
