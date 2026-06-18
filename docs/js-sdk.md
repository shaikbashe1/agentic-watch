# JavaScript SDK Documentation

The `agentwatch` JS SDK provides an asynchronous interface for Node.js agents (like LangChain.js or Custom TS Agents).

## Installation
```bash
npm install agentwatch
```

## Initialization
```typescript
import { AgentWatch } from 'agentwatch';

// Initialize with explicit key
const aw = new AgentWatch("ak_12345...");

// Or initialize using environment variables
// process.env.AGENTWATCH_API_KEY="ak_12345..."
const aw = new AgentWatch();
```

## Tracking Events
Because Node.js is asynchronous, `track()` returns a Promise. However, it suppresses errors internally to prevent crashing your main agent loop.

### Tracking a Tool Call
```typescript
await aw.track({
    event_type: "tool_call",
    agent_id: "agent_abc123",
    tool_name: "DatabaseQuery",
    status: "success",
    latency_ms: 120
});
```
