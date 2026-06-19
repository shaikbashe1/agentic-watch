import uuid
import time
import json
from ..client import AgentWatchClient

class BaseParser:
    def __init__(self, client: AgentWatchClient):
        self.client = client
        
    def handle_request(self, original_handler, pool, request):
        start_time = time.time()
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        request_body = self.extract_request_body(request)
        
        # Pre-flight synchronous policy check
        decision = self.client.check_policy({
            "request": request_body,
            "url": str(request.url)
        })
        if decision.get("action") == "BLOCK":
            from ..exceptions import AgentWatchPolicyViolation
            reason = decision.get("reason", "Policy Violation")
            
            latency = int((time.time() - start_time) * 1000)
            event = self.build_error_event(request, f"BLOCKED: {reason}", trace_id, span_id, latency)
            if event:
                self.client.send_event(event)
                
            raise AgentWatchPolicyViolation(f"AgentWatch blocked request: {reason}")
            
        try:
            response = original_handler(pool, request)
            latency = int((time.time() - start_time) * 1000)
            
            response_body = self.extract_response_body(response)
            
            event = self.build_event(request, response, request_body, response_body, trace_id, span_id, latency)
            if event:
                self.client.send_event(event)
                
            return response
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            event = self.build_error_event(request, str(e), trace_id, span_id, latency)
            if event:
                self.client.send_event(event)
            raise e

    def extract_request_body(self, request):
        try:
            # Depending on httpcore version and request structure
            if hasattr(request, "stream") and hasattr(request.stream, "read"):
                # Warning: reading stream might consume it. In a real monkey patch
                # we'd need a robust way to peek or wrap the stream.
                # For Phase 1 we will try to read the payload if available.
                pass
            
            # Simple fallback if content is available
            if getattr(request, "content", None):
                return json.loads(request.content)
                
            return {}
        except:
            return {}

    def extract_response_body(self, response):
        try:
            # We must be careful not to consume the iter_stream
            # Real implementation requires wrapping the stream
            return {}
        except:
            return {}
            
    def build_event(self, request, response, req_body, res_body, trace_id, span_id, latency):
        raise NotImplementedError
        
    def build_error_event(self, request, error_msg, trace_id, span_id, latency):
        raise NotImplementedError
