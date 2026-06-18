# Agentic Watch Quick Start

Welcome to Agentic Watch! This guide will help you connect your first AI Agent in under 5 minutes.

## 1. Create a Workspace
Sign up on the Agentic Watch dashboard and create your company workspace.

## 2. Register Your Agent
Navigate to **Settings > Connect Agent** (or `/agents/wizard`) in the dashboard.
Enter your Agent's name and select its underlying framework (e.g., LangGraph, CrewAI).

## 3. Generate API Key
Upon registration, Agentic Watch will generate a unique `agent_id` and a secure `API_KEY`. Save this key securely.

## 4. Integrate SDK
Install the SDK for your language:
`pip install agentwatch` or `npm install agentwatch`.

Drop the tracker into your agent's execution loop:
```python
from agentwatch import AgentWatch

aw = AgentWatch(api_key="your_api_key")

aw.track(
    event_type="tool_call",
    agent_id="your_agent_id",
    tool_name="Search",
    status="success",
    latency=150
)
```

## 5. View Telemetry
Go back to the Agentic Watch Dashboard to see your events streaming live!
