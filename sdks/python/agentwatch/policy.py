class LocalPolicyEnforcer:
    def __init__(self, client):
        self.client = client
        self.policies = []
        
    def load_policies(self, policies):
        self.policies = policies
        
    def evaluate(self, event_data: dict) -> dict:
        """
        Evaluate local policies synchronously before the request goes out.
        """
        for policy in self.policies:
            if self._matches(policy, event_data):
                return {
                    "action": policy.get("action", "ALLOW"),
                    "reason": policy.get("name", "Policy Violation")
                }
        return {"action": "ALLOW"}
        
    def _matches(self, policy, event_data):
        conditions = policy.get("conditions", [])
        for condition in conditions:
            field = condition.get("field")
            operator = condition.get("operator")
            value = condition.get("value")
            
            # Simple extractor for Phase 3
            actual_value = event_data.get(field)
            if actual_value is None:
                # try nested
                if field == "url" and "url" in event_data:
                    actual_value = event_data["url"]
                    
            if operator == "contains":
                if not actual_value or value not in str(actual_value):
                    return False
            elif operator == "eq":
                if actual_value != value:
                    return False
        return True
