import uuid
import time
from typing import Any, Dict, List, Optional
try:
    from langchain.callbacks.base import BaseCallbackHandler
except ImportError:
    BaseCallbackHandler = object

class AgentWatchLangChainCallback(BaseCallbackHandler):
    """
    LangChain callback handler that streams events to AgentWatch.
    """
    def __init__(self, client):
        self.client = client
        self.runs = {}

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        run_id = str(kwargs.get("run_id", uuid.uuid4()))
        self.runs[run_id] = {"start_time": time.time(), "type": "llm_call", "prompts": prompts}

    def on_llm_end(self, response: Any, **kwargs: Any) -> Any:
        run_id = str(kwargs.get("run_id"))
        if run_id in self.runs:
            start_time = self.runs[run_id]["start_time"]
            latency = int((time.time() - start_time) * 1000)
            
            event = {
                "trace_id": str(kwargs.get("parent_run_id", run_id)),
                "span_id": run_id,
                "event_type": "llm_call",
                "framework": "langchain",
                "latency_ms": latency,
                "payload": {
                    "prompts": self.runs[run_id].get("prompts"),
                    "response": str(response)
                }
            }
            self.client.send_event(event)

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        run_id = str(kwargs.get("run_id", uuid.uuid4()))
        self.runs[run_id] = {
            "start_time": time.time(), 
            "type": "tool_call",
            "tool_name": serialized.get("name", "unknown") if serialized else "unknown",
            "input": input_str
        }

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        run_id = str(kwargs.get("run_id"))
        if run_id in self.runs:
            run_data = self.runs[run_id]
            latency = int((time.time() - run_data["start_time"]) * 1000)
            
            event = {
                "trace_id": str(kwargs.get("parent_run_id", run_id)),
                "span_id": run_id,
                "event_type": "tool_call",
                "framework": "langchain",
                "tool_name": run_data["tool_name"],
                "latency_ms": latency,
                "payload": {
                    "input": run_data["input"],
                    "output": output
                }
            }
            self.client.send_event(event)
