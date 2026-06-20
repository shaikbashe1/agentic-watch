import httpx
import threading
import time
from typing import List
from .parsers.base import LLMEvent
import agentwatch

class AgentWatchClient:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __init__(self):
        self.queue: List[LLMEvent] = []
        self.http_client = httpx.Client(base_url="http://localhost:8000/api/v1")
        
        self._worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._worker_thread.start()

    def enqueue_event(self, event: LLMEvent):
        self.queue.append(event)
        
    def _worker_loop(self):
        while True:
            time.sleep(agentwatch._config.flush_interval)
            self.flush()

    def flush(self):
        if not self.queue:
            return
            
        batch = self.queue[:agentwatch._config.batch_size]
        self.queue = self.queue[agentwatch._config.batch_size:]
        
        try:
            payload = {
                "events": [
                    {
                        "id": "00000000-0000-0000-0000-000000000000", # Will use UUID in actual
                        "trace_id": "trace-1",
                        "span_id": "span-1",
                        "session_id": "session-1",
                        "event_type": "llm_call",
                        "framework": "httpcore",
                        "started_at": event.started_at.isoformat(),
                        "ended_at": event.ended_at.isoformat(),
                        "latency_ms": event.latency_ms,
                        "workspace_id": agentwatch._config.workspace_id,
                        "agent_name": agentwatch._config.agent_name,
                        "payload": event.model_dump()
                    }
                    for event in batch
                ]
            }
            
            headers = {"Authorization": f"Bearer {agentwatch._config.api_key}"}
            self.http_client.post("/ingest/batch", json=payload, headers=headers)
        except Exception as e:
            print(f"AgentWatch failed to flush events: {e}")
            # Put back in queue to retry
            self.queue = batch + self.queue
