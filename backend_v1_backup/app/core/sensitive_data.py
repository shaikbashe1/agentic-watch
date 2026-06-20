import re
from typing import List, Dict

class SensitiveDataDetector:
    PATTERNS = {
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "api_key": r"\b(?:sk-|aw_|AIza)[A-Za-z0-9]{20,}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b",
        "aws_key": r"\bAKIA[0-9A-Z]{16}\b",
        "private_key": r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    }
    
    def __init__(self):
        self.compiled_patterns = {k: re.compile(v) for k, v in self.PATTERNS.items()}
        
    def scan(self, text: str) -> List[Dict[str, str]]:
        if not text:
            return []
            
        matches = []
        for name, pattern in self.compiled_patterns.items():
            for match in pattern.finditer(text):
                matches.append({
                    "type": name,
                    "match": match.group(0),
                    "start": match.start(),
                    "end": match.end()
                })
        return matches
        
    def redact(self, text: str) -> str:
        if not text:
            return text
            
        redacted = text
        for name, pattern in self.compiled_patterns.items():
            redacted = pattern.sub(f"[REDACTED-{name.upper()}]", redacted)
            
        return redacted
