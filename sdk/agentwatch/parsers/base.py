from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class LLMEvent(BaseModel):
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    started_at: datetime
    ended_at: datetime
    latency_ms: int
    request_payload: Dict[str, Any]
    response_payload: Dict[str, Any]

class BaseParser:
    def can_handle(self, request) -> bool:
        """Return True if this parser can handle the given httpcore request."""
        return False
        
    def parse(self, request, response, start_time: datetime, end_time: datetime, latency_ms: int) -> Optional[LLMEvent]:
        """Parse the httpcore request and response into an LLMEvent."""
        return None
