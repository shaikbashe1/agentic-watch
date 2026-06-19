from typing import List, Dict, Any
import re

class PolicyDecision:
    def __init__(self, action: str, reason: str, policy_id: str = None):
        self.action = action  # ALLOW, WARN, BLOCK
        self.reason = reason
        self.policy_id = policy_id

class PolicyEngine:
    def evaluate(self, policies: List[Any], event_data: dict) -> PolicyDecision:
        """
        Evaluate a list of policies against an event.
        Policies must be ordered by priority (lower priority number = evaluated first).
        """
        for policy in sorted(policies, key=lambda p: p.priority if hasattr(p, 'priority') else 100):
            if not getattr(policy, "enabled", True) and not policy.get("enabled", True):
                continue
                
            conditions = getattr(policy, "conditions", [])
            if isinstance(policy, dict):
                conditions = policy.get("conditions", [])
                
            if not conditions:
                continue
                
            if self._matches_all(conditions, event_data):
                action = getattr(policy, "action", "ALLOW")
                if isinstance(policy, dict):
                    action = policy.get("action", "ALLOW")
                    
                name = getattr(policy, "name", "Unnamed Policy")
                if isinstance(policy, dict):
                    name = policy.get("name", "Unnamed Policy")
                    
                pid = getattr(policy, "id", None)
                if isinstance(policy, dict):
                    pid = policy.get("id", None)
                    
                return PolicyDecision(
                    action=action,
                    reason=f"Matched policy: {name}",
                    policy_id=str(pid) if pid else None
                )
                
        return PolicyDecision("ALLOW", "Default allow")
        
    def _matches_all(self, conditions: List[dict], event_data: dict) -> bool:
        for condition in conditions:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            
            actual_value = self._extract_field(event_data, field)
            
            if not self._evaluate_condition(actual_value, operator, value):
                return False
        return True
        
    def _extract_field(self, data: dict, field_path: str) -> Any:
        parts = field_path.split(".")
        current = data
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None
        return current
        
    def _evaluate_condition(self, actual_value: Any, operator: str, expected_value: Any) -> bool:
        if actual_value is None:
            return False
            
        try:
            if operator == "eq":
                return str(actual_value) == str(expected_value)
            elif operator == "neq":
                return str(actual_value) != str(expected_value)
            elif operator == "contains":
                return str(expected_value).lower() in str(actual_value).lower()
            elif operator == "not_contains":
                return str(expected_value).lower() not in str(actual_value).lower()
            elif operator == "gt":
                return float(actual_value) > float(expected_value)
            elif operator == "lt":
                return float(actual_value) < float(expected_value)
            elif operator == "regex":
                return bool(re.search(str(expected_value), str(actual_value)))
            elif operator == "in":
                return str(actual_value) in expected_value if isinstance(expected_value, list) else False
            return False
        except (ValueError, TypeError):
            return False
