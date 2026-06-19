import json
from .base import BaseParser

class AnthropicParser(BaseParser):
    def build_event(self, request, response, req_body, res_body, trace_id, span_id, latency):
        model = req_body.get("model", "unknown")
        
        input_tokens = 0
        output_tokens = 0
        
        event = {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "llm_call",
            "provider": "anthropic",
            "model": model,
            "latency_ms": latency,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "payload": {
                "request": req_body,
                "response": res_body,
                "status_code": getattr(response, "status", 200)
            }
        }
        return event

    def build_error_event(self, request, error_msg, trace_id, span_id, latency):
        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "llm_call",
            "provider": "anthropic",
            "latency_ms": latency,
            "error": error_msg,
            "payload": {}
        }
