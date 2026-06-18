import os
import time
import requests
import functools

API_URL = os.environ.get("AGENTWATCH_API_URL", "http://localhost:8000")

def monitor(agent):
    """
    Wraps an agent to automatically send telemetry to Agentic Watch.
    """
    class MonitoredAgent:
        def __init__(self, original_agent):
            self._original_agent = original_agent
            self.agent_id = getattr(original_agent, "id", "default_agent")

        def run(self, *args, **kwargs):
            start_time = time.time()
            requests.post(f"{API_URL}/timeline", json={
                "agent_id": self.agent_id,
                "step_type": "Planning",
                "status": "Started",
                "duration_ms": 0
            })

            try:
                result = self._original_agent.run(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                requests.post(f"{API_URL}/timeline", json={
                    "agent_id": self.agent_id,
                    "step_type": "Final Output",
                    "status": "Success",
                    "duration_ms": duration
                })
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                requests.post(f"{API_URL}/timeline", json={
                    "agent_id": self.agent_id,
                    "step_type": "Final Output",
                    "status": "Failed",
                    "duration_ms": duration
                })
                raise e

        def __getattr__(self, name):
            return getattr(self._original_agent, name)

    return MonitoredAgent(agent)

def tool_trace(tool_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            agent_id = kwargs.get('agent_id', 'default_agent')
            input_data = str(args) + str(kwargs)
            try:
                result = func(*args, **kwargs)
                duration = (time.time() - start_time) * 1000
                requests.post(f"{API_URL}/tool-traces", json={
                    "agent_id": agent_id,
                    "tool_name": tool_name,
                    "input_data": input_data,
                    "output_data": str(result),
                    "latency_ms": duration,
                    "success": True
                })
                return result
            except Exception as e:
                duration = (time.time() - start_time) * 1000
                requests.post(f"{API_URL}/tool-traces", json={
                    "agent_id": agent_id,
                    "tool_name": tool_name,
                    "input_data": input_data,
                    "output_data": str(e),
                    "latency_ms": duration,
                    "success": False
                })
                raise e
        return wrapper
    return decorator
