import json
from .base import BaseParser, LLMEvent
from datetime import datetime
from typing import Optional

class OpenAIParser(BaseParser):
    def can_handle(self, request) -> bool:
        host = request.url.host.decode('utf-8') if isinstance(request.url.host, bytes) else request.url.host
        return "api.openai.com" in host and "/v1/chat/completions" in request.url.target.decode('utf-8')

    def parse(self, request, response, start_time: datetime, end_time: datetime, latency_ms: int) -> Optional[LLMEvent]:
        try:
            req_body = json.loads(request.read().decode('utf-8'))
            resp_body = json.loads(response.read().decode('utf-8'))
            
            return LLMEvent(
                provider="openai",
                model=resp_body.get("model", req_body.get("model", "unknown")),
                input_tokens=resp_body.get("usage", {}).get("prompt_tokens", 0),
                output_tokens=resp_body.get("usage", {}).get("completion_tokens", 0),
                started_at=start_time,
                ended_at=end_time,
                latency_ms=latency_ms,
                request_payload=req_body,
                response_payload=resp_body
            )
        except Exception:
            return None
