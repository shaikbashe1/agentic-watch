import uuid
import time
import json

class MCPInterceptor:
    def __init__(self, client):
        self.client = client
        
    def intercept_mcp_call(self, original_func, *args, **kwargs):
        start_time = time.time()
        trace_id = str(uuid.uuid4())
        span_id = str(uuid.uuid4())
        
        # MCP JSON-RPC Payload format
        payload = kwargs.get("payload", {})
        if not payload and len(args) > 0:
            payload = args[0]
            
        method = payload.get("method", "unknown")
        
        try:
            result = original_func(*args, **kwargs)
            latency = int((time.time() - start_time) * 1000)
            
            self.client.send_event({
                "trace_id": trace_id,
                "span_id": span_id,
                "event_type": "mcp_call",
                "tool_name": method,
                "latency_ms": latency,
                "payload": {
                    "request": payload,
                    "response": result
                }
            })
            return result
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            self.client.send_event({
                "trace_id": trace_id,
                "span_id": span_id,
                "event_type": "error",
                "tool_name": method,
                "latency_ms": latency,
                "error": str(e)
            })
            raise e
