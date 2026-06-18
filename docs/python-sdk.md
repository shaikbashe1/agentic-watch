# Python SDK Documentation

The `agentwatch` Python SDK provides a simple, synchronous interface for sending telemetry data from your Python agents (LangGraph, CrewAI, AutoGen, Custom) to the Agentic Watch platform.

## Installation
```bash
pip install agentwatch
```

## Initialization
```python
from agentwatch import AgentWatch

# Initialize with explicit key
aw = AgentWatch(api_key="ak_12345...")

# Or initialize using environment variables
# export AGENTWATCH_API_KEY="ak_12345..."
aw = AgentWatch()
```

## Tracking Events
The `track()` method sends telemetry payload to the platform.

### Tracking a Tool Call
```python
aw.track(
    event_type="tool_call",
    agent_id="agent_abc123",
    tool_name="GoogleSearch",
    status="success",
    latency=250, # ms
    input_data="{'query': 'weather in NYC'}",
    output_data="Sunny, 75F"
)
```

### Tracking Token Usage
```python
aw.track(
    event_type="token_usage",
    agent_id="agent_abc123",
    prompt_tokens=150,
    completion_tokens=45,
    cost_usd=0.002
)
```
