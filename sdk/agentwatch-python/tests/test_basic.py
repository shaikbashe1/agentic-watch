import time
import os
from agentwatch import init, trace_workflow, trace_agent, trace_tool

# Initialize AgentWatch SDK (points to local otel-collector)
telemetry = init({
    "service_name": "test-ai-service",
    "endpoint": "http://localhost:4317"
})

@trace_tool(name="search_web")
def search_web(query: str):
    print(f"Searching web for: {query}")
    time.sleep(0.5)
    return "Search results for " + query

@trace_agent(name="ResearchAgent")
def do_research(topic: str):
    print(f"Agent starting research on: {topic}")
    time.sleep(0.1)
    results = search_web(topic)
    time.sleep(0.2)
    return f"Research Complete: {results}"

@trace_workflow(name="ContentGenerationWorkflow")
def main():
    print("Starting Workflow")
    do_research("OpenTelemetry in Python")
    print("Workflow Finished")

if __name__ == "__main__":
    main()
    
    # Allow time for batch processor to flush traces to OTLP
    time.sleep(2)
