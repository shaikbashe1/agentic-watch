import re
from typing import Dict, Any

class RiskScorer:
    """
    Evaluates agent payloads in real-time to generate a risk score from 0-100.
    High scores indicate potential PII leaks, credential leaks, or malicious intent.
    """
    
    # Naive regexes for fast evaluation (In production, use Presidio or ML models)
    PATTERNS = {
        "ssn": re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        "credit_card": re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
        "api_key": re.compile(r'(?i)(?:key|token|password|secret)[\s=:]+[a-zA-Z0-9_\-]{16,}'),
    }
    
    @classmethod
    def evaluate(cls, payload: Dict[str, Any]) -> int:
        score = 0
        text_to_analyze = str(payload).lower()
        
        # High-risk patterns
        if cls.PATTERNS["ssn"].search(text_to_analyze):
            score += 50
        if cls.PATTERNS["credit_card"].search(text_to_analyze):
            score += 60
        if cls.PATTERNS["api_key"].search(text_to_analyze):
            score += 80
            
        # Hard limits
        if "rm -rf" in text_to_analyze or "drop table" in text_to_analyze:
            score += 100
            
        return min(score, 100)
