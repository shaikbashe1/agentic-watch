from typing import Dict, Any, List
from pydantic import BaseModel
from .sensitive_data import SensitiveDataDetector

class RiskFactor(BaseModel):
    name: str
    score: int
    description: str

class RiskScore(BaseModel):
    score: int
    factors: List[RiskFactor]

class RiskScorer:
    def __init__(self):
        self.sensitive_detector = SensitiveDataDetector()
        
    def score_event(self, event_data: dict) -> RiskScore:
        factors = []
        
        event_type = event_data.get("event_type", "unknown")
        payload = str(event_data.get("payload", {}))
        
        # 1. Error Risk
        if event_type == "error" or event_data.get("error"):
            factors.append(RiskFactor(
                name="execution_error", 
                score=30, 
                description="The agent or tool encountered an execution error."
            ))
            
        # 2. Tool Danger Level
        if event_type in ["tool_call", "mcp_call"]:
            tool_name = event_data.get("tool_name", "").lower()
            dangerous_tools = ["shell", "bash", "cmd", "exec", "eval", "delete", "drop"]
            if any(dt in tool_name for dt in dangerous_tools):
                factors.append(RiskFactor(
                    name="dangerous_tool", 
                    score=70, 
                    description=f"Tool '{tool_name}' matches a known high-risk pattern."
                ))
                
        # 3. Sensitive Data Risk
        pii_matches = self.sensitive_detector.scan(payload)
        if pii_matches:
            factors.append(RiskFactor(
                name="sensitive_data", 
                score=50, 
                description=f"Detected {len(pii_matches)} sensitive data patterns (e.g. {pii_matches[0]['type']})."
            ))
            
        # 4. LLM Cost / Complexity Risk (approximate by tokens)
        input_tokens = event_data.get("input_tokens", 0) or 0
        if input_tokens > 32000:
            factors.append(RiskFactor(
                name="high_context_window", 
                score=20, 
                description="Extremely large context window usage implies high complexity/cost."
            ))
            
        # Compute final score
        total_score = sum(f.score for f in factors)
        if not factors:
            total_score = 0
            
        final_score = min(max(total_score, 0), 100)
        
        return RiskScore(score=final_score, factors=factors)
