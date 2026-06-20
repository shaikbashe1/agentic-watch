import re

class PIIFilter:
    def __init__(self):
        # Basic patterns for SSN, Credit Cards, Emails
        self.patterns = {
            "email": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
            "credit_card": r'\b(?:\d[ -]*?){13,16}\b'
        }
        
    def detect_pii(self, text: str):
        detected = []
        for pii_type, pattern in self.patterns.items():
            if re.search(pattern, text):
                detected.append(pii_type)
        return detected

class PromptInjectionDetector:
    def __init__(self):
        self.heuristics = [
            "ignore previous instructions",
            "system prompt",
            "you are an attacker",
            "forget everything"
        ]
        
    def detect_injection(self, prompt: str) -> float:
        """Returns a risk score from 0.0 to 1.0"""
        prompt_lower = prompt.lower()
        score = 0.0
        for h in self.heuristics:
            if h in prompt_lower:
                score += 0.25
        return min(score, 1.0)
