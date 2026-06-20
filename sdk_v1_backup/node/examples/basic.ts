import { AgentWatchClient, withTrace } from "../src";

// Initialize the global client
const client = AgentWatchClient.init({
  apiKey: "test_key",
  apiUrl: "https://backend-psi-two-49.vercel.app" 
});

// A dummy LLM call
const callLLM = withTrace({ name: "LLM Completion", eventType: "llm_call" }, async (prompt: string) => {
  console.log(`[LLM] Thinking about: ${prompt}`);
  await new Promise(resolve => setTimeout(resolve, 800)); // Simulate network latency
  
  // You can also manually record an event within the active context
  client.recordEvent({
    event_type: "token_usage",
    payload: { input_tokens: 15, output_tokens: 42 }
  });

  return `Here is a witty response to: ${prompt}`;
});

// A dummy tool execution
const executeSearch = withTrace({ name: "Web Search Tool", eventType: "tool_call" }, async (query: string) => {
  console.log(`[Tool] Searching web for: ${query}`);
  await new Promise(resolve => setTimeout(resolve, 500));
  return `Found 3 results for ${query}`;
});

// The main agent orchestrator
const runAgent = withTrace({ name: "Research Agent Execution", eventType: "agent_run" }, async (task: string) => {
  console.log(`[Agent] Starting task: ${task}`);
  
  // This will be automatically nested under the agent's span!
  const searchResults = await executeSearch(task);
  
  // This will also be nested!
  const finalAnswer = await callLLM(`Synthesize these results: ${searchResults}`);
  
  console.log(`[Agent] Finished task!`);
  return finalAnswer;
});

async function main() {
  await runAgent("What is the capital of France?");
  
  // Wait for the background flusher to send the events, or force flush
  await client.shutdown();
  console.log("Done.");
}

main().catch(console.error);
