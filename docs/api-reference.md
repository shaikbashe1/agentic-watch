# API Reference

Agentic Watch exposes a robust REST API for managing the platform.

## Agent Registration

**Endpoint:** `POST /agents/register`

Registers a new agent under your workspace.

**Request Body:**
```json
{
  "name": "CustomerSupportAgent",
  "framework": "LangGraph",
  "description": "Support automation agent"
}
```

**Response:**
```json
{
  "agent_id": "agent_8f7b...",
  "api_key": "ak_1d2c..."
}
```

## Telemetry Ingestion

**Endpoint:** `POST /telemetry`
**Headers:** `X-API-Key: <your_api_key>`

A universal ingestion endpoint that parses the `event_type` to route data correctly.

**Example: Tool Trace**
```json
{
  "event_type": "tool_call",
  "agent_id": "agent_8f7b...",
  "tool_name": "SearchAPI",
  "status": "success",
  "latency": 120,
  "timestamp": 1684323491
}
```
