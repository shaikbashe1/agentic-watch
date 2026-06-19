import json
from .base import BaseParser

class GeminiParser(BaseParser):
    def build_event(self, request, response, req_body, res_body, trace_id, span_id, latency):
        # Gemini format uses "contents" for messages
        model = "gemini-1.5-pro"  # Default fallback
        if "models/" in str(request.url):
            model = str(request.url).split("models/")[1].split(":")[0]
            
        input_tokens = 0
        output_tokens = 0
        
        # Gemini format includes usageMetadata in response
        if "usageMetadata" in res_body:
            input_tokens = res_body["usageMetadata"].get("promptTokenCount", 0)
            output_tokens = res_body["usageMetadata"].get("candidatesTokenCount", 0)
        # Approximate tokens if not provided by stream
        elif req_body.get("contents"):
            # rough estimate
            input_tokens = len(json.dumps(req_body["contents"])) // 4
            
        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "llm_call",
            "llm_provider": "google",
            "llm_model": model,
            "latency_ms": latency,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "payload": {
                "request": req_body,
                "response": res_body,
                "url": str(request.url)
            }
        }
        
    def build_error_event(self, request, error_msg, trace_id, span_id, latency):
        model = "gemini-unknown"
        if "models/" in str(request.url):
            model = str(request.url).split("models/")[1].split(":")[0]
            
        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "error",
            "llm_provider": "google",
            "llm_model": model,
            "latency_ms": latency,
            "error": error_msg,
            "payload": {
                "url": str(request.url)
            }
        }
