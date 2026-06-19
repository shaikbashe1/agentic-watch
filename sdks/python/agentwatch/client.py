import os
import time
import queue
import threading
import requests
import logging
import json
import httpx
from .policy import LocalPolicyEnforcer
from .risk import LocalRiskScorer

class AgentWatchClient:
    def __init__(self, api_key: str, api_url: str, session_id: str, environment: str, tags: dict):
        self.api_key = api_key
        self.api_url = api_url.rstrip("/")
        self.session_id = session_id
        self.environment = environment
        self.tags = tags
        
        self.policy_enforcer = LocalPolicyEnforcer(self)
        self.risk_scorer = LocalRiskScorer()
        
        self.headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def check_policy(self, event_data: dict) -> dict:
        return self.policy_enforcer.evaluate(event_data)

    def send_event(self, event: dict):
        event["session_id"] = self.session_id
        event["environment"] = self.environment
        event["tags"] = self.tags
        
        # Local heuristic risk scoring
        event["risk_score"] = self.risk_scorer.score_event(event)
        
        try:
            self.queue.put_nowait(event)
        except queue.Full:
            logging.warning("AgentWatch: Event queue full, dropping event.")

    def _worker(self):
        batch = []
        while True:
            try:
                # Wait for up to 1 second for an item
                item = self.queue.get(timeout=1.0)
                batch.append(item)
                
                # Drain queue up to 100 items
                while not self.queue.empty() and len(batch) < 100:
                    batch.append(self.queue.get_nowait())
                    
                self._send_batch(batch)
                batch = []
            except queue.Empty:
                if batch:
                    self._send_batch(batch)
                    batch = []

    def _send_batch(self, batch: list):
        try:
            requests.post(
                f"{self.api_url}/ingest/batch",
                headers=self.headers,
                json={"events": batch},
                timeout=5
            )
        except Exception as e:
            logging.debug(f"AgentWatch failed to send batch: {e}")

    def check_policy(self, payload: dict) -> dict:
        """
        Synchronously checks policy against the backend.
        """
        try:
            resp = requests.post(
                f"{self.api_url}/policies/evaluate",
                headers=self.headers,
                json={"payload": payload},
                timeout=2
            )
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            logging.debug(f"AgentWatch policy check failed: {e}")
            
        return {"action": "ALLOW"}
