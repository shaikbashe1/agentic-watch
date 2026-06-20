from typing import Dict, Any, Tuple
from app.core.risk_scorer import RiskScorer

class PolicyEngine:
    """
    Evaluates events against workspace policies.
    Returns (decision, reason, risk_score)
    decision can be: "allow", "warn", "block"
    """
    
    @classmethod
    def evaluate(cls, payload: Dict[str, Any], workspace_id: str) -> Tuple[str, str, int]:
        # 1. Calculate Risk Score
        risk_score = RiskScorer.evaluate(payload)
        
        # 2. In a real environment, fetch workspace policies from Postgres here
        # For Phase 3 scaffold, we use hardcoded defaults
        
        if risk_score >= 80:
            return "block", "High risk score: potential credential leak or malicious command", risk_score
        elif risk_score >= 50:
            return "warn", "Medium risk score: potential PII detected", risk_score
            
        # Example policy: Block usage of specific LLMs
        model = payload.get("model", "")
        if "gpt-4" in model and "gpt-4-turbo" not in model:
             # Just an example of a cost-control policy
             return "warn", "Deprecated model usage detected. Consider upgrading.", risk_score
             
        # Example policy: Block specific tool names
        tool_name = payload.get("tool_name", "")
        if tool_name == "delete_database":
            return "block", "Unauthorized tool execution", risk_score
            
        return "allow", "All policies passed", risk_score
