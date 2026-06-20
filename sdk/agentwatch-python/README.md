# AgentWatch Python SDK (V2)

Enterprise OpenTelemetry SDK for AI Agents.

## Installation
```bash
pip install agentwatch
```

## Usage
```python
from agentwatch import init, trace_agent

# Initialize telemetry
telemetry = init({
    "service_name": "my-agent-service",
    "endpoint": "http://localhost:4317"
})

@trace_agent(name="ResearchAgent")
def run_research(query: str):
    pass
```
