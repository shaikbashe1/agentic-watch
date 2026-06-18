import os
import time
import requests
import functools
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Optional, Callable

# Global executor for zero-latency background telemetry
_executor = ThreadPoolExecutor(max_workers=5)

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

    def _send_payload(self, payload: dict):
        try:
            requests.post(f"{self.api_url}/telemetry", headers=self.headers, json=payload, timeout=3)
        except Exception:
            pass

    def track(self, event_type: str, agent_id: str, **kwargs) -> None:
        """
        Send a telemetry event to Agentic Watch asynchronously.
        """
        payload = {
            "event_type": event_type,
            "agent_id": agent_id,
            "timestamp": time.time(),
            **kwargs
        }
        
        # Fire and forget
        _executor.submit(self._send_payload, payload)

# Global singleton for decorator usage
_default_aw = None

def monitor(agent_id: str, api_key: str = None):
    """
    Decorator to easily monitor an agent function or class.
    Example:
        @monitor(agent_id="my_agent")
        def run_agent(input_data):
            ...
    """
    global _default_aw
    if not _default_aw:
        _default_aw = AgentWatch(api_key=api_key)
        
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            _default_aw.track(event_type="timeline_step", agent_id=agent_id, step="Agent execution started")
            
            try:
                result = func(*args, **kwargs)
                latency = time.time() - start_time
                _default_aw.track(
                    event_type="timeline_step", 
                    agent_id=agent_id, 
                    step="Agent execution completed", 
                    latency=latency,
                    status="success"
                )
                return result
            except Exception as e:
                latency = time.time() - start_time
                _default_aw.track(
                    event_type="timeline_step", 
                    agent_id=agent_id, 
                    step=f"Agent execution failed: {str(e)}", 
                    latency=latency,
                    status="error"
                )
                raise e
        return wrapper
    return decorator
