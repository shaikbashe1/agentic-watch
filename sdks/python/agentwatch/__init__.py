import os
import time
import requests
from typing import Any, Dict, Optional

class AgentWatch:
    def __init__(self, api_key: str = None, api_url: str = None):
        self.api_key = api_key or os.environ.get("AGENTWATCH_API_KEY")
        self.api_url = api_url or os.environ.get("AGENTWATCH_API_URL", "http://localhost:8000")
        
        if not self.api_key:
            raise ValueError("AgentWatch requires an API Key. Pass it to the constructor or set AGENTWATCH_API_KEY.")
            
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

    def track(self, event_type: str, agent_id: str, **kwargs) -> None:
        """
        Send a telemetry event to Agentic Watch.
        
        :param event_type: Type of the event (e.g., 'tool_call', 'timeline_step', 'token_usage')
        :param agent_id: The ID of the agent this event belongs to
        :param kwargs: Additional event payload data (tool_name, latency, status, etc.)
        """
        payload = {
            "event_type": event_type,
            "agent_id": agent_id,
            "timestamp": time.time(),
            **kwargs
        }
        
        try:
            requests.post(f"{self.api_url}/telemetry", headers=self.headers, json=payload, timeout=3)
        except Exception as e:
            # We fail silently so observability doesn't crash the main agent
            pass
