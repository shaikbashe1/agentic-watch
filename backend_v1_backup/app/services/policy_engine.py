import json
import logging
import redis
import os
from sqlalchemy.orm import Session
from ..models.policy import Policy

logger = logging.getLogger(__name__)

# Redis configuration
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
try:
    redis_client = redis.from_url(REDIS_URL)
except Exception as e:
    logger.warning(f"Failed to connect to Redis: {e}")
    redis_client = None

class PolicyEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_workspace_policies(self, workspace_id: str) -> list:
        cache_key = f"policies:workspace:{workspace_id}"
        
        if redis_client:
            try:
                cached = redis_client.get(cache_key)
                if cached:
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Redis get failed: {e}")

        # Fetch from DB if not in cache
        policies = self.db.query(Policy).filter(
            Policy.workspace_id == workspace_id, 
            Policy.is_active == True
        ).all()
        
        policy_data = []
        for p in policies:
            policy_data.append({
                "id": p.id,
                "action": p.action,
                "conditions": p.conditions
            })
            
        if redis_client:
            try:
                # Cache for 60 seconds
                redis_client.setex(cache_key, 60, json.dumps(policy_data))
            except Exception as e:
                logger.warning(f"Redis set failed: {e}")
                
        return policy_data

    def evaluate(self, workspace_id: str, payload: dict) -> dict:
        """
        Evaluate a payload against all active policies for the workspace.
        Returns {"action": "ALLOW"} or {"action": "BLOCK", "matched_policy_id": "...", "reason": "..."}
        """
        policies = self.get_workspace_policies(workspace_id)
        
        for policy in policies:
            if self._match_condition(policy["conditions"], payload):
                return {
                    "action": policy["action"],
                    "matched_policy_id": policy["id"],
                    "reason": f"Matched policy {policy['id']}"
                }
                
        return {"action": "ALLOW"}

    def _match_condition(self, condition: dict, payload: dict) -> bool:
        """
        Simple AST evaluator. 
        Example condition: {"field": "model", "operator": "==", "value": "gpt-4"}
        """
        if not condition:
            return False
            
        field = condition.get("field")
        op = condition.get("operator")
        val = condition.get("value")
        
        if not field or not op:
            return False
            
        # Support dot notation for nested fields, e.g. "request.model"
        actual_val = payload
        for part in field.split("."):
            if isinstance(actual_val, dict):
                actual_val = actual_val.get(part)
            else:
                actual_val = None
                break
                
        if op == "==":
            return str(actual_val) == str(val)
        elif op == "!=":
            return str(actual_val) != str(val)
        elif op == "in" and isinstance(val, list):
            return actual_val in val
        elif op == ">" and isinstance(actual_val, (int, float)) and isinstance(val, (int, float)):
            return actual_val > val
        elif op == "<" and isinstance(actual_val, (int, float)) and isinstance(val, (int, float)):
            return actual_val < val
            
        return False
