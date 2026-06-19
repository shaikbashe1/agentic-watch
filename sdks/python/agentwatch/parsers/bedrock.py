import json
from .base import BaseParser

class BedrockParser(BaseParser):
    def build_event(self, request, response, req_body, res_body, trace_id, span_id, latency):
        model = "bedrock-unknown"
        if "model/" in str(request.url):
            model = str(request.url).split("model/")[1].split("/invoke")[0]
            
        input_tokens = 0
        output_tokens = 0
        
        # Bedrock response body differs per model (e.g., anthropic.claude vs meta.llama)
        # We try to extract common token counts if available
        # This is a stub for the exact payload parsing
            
        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "llm_call",
            "llm_provider": "aws_bedrock",
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
        model = "bedrock-unknown"
        if "model/" in str(request.url):
            model = str(request.url).split("model/")[1].split("/invoke")[0]
            
        return {
            "trace_id": trace_id,
            "span_id": span_id,
            "event_type": "error",
            "llm_provider": "aws_bedrock",
            "llm_model": model,
            "latency_ms": latency,
            "error": error_msg,
            "payload": {
                "url": str(request.url)
            }
        }
