import uuid
import time
import functools

def patch_autogen(client):
    try:
        from autogen import ConversableAgent
        
        original_generate_reply = ConversableAgent.generate_reply
        
        @functools.wraps(original_generate_reply)
        def patched_generate_reply(self, *args, **kwargs):
            start_time = time.time()
            trace_id = str(uuid.uuid4())
            span_id = str(uuid.uuid4())
            
            try:
                result = original_generate_reply(self, *args, **kwargs)
                latency = int((time.time() - start_time) * 1000)
                
                client.send_event({
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "event_type": "agent_start",
                    "framework": "autogen",
                    "agent_name": self.name,
                    "latency_ms": latency,
                    "payload": {"reply": str(result)}
                })
                return result
            except Exception as e:
                latency = int((time.time() - start_time) * 1000)
                client.send_event({
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "event_type": "error",
                    "framework": "autogen",
                    "agent_name": self.name,
                    "latency_ms": latency,
                    "error": str(e)
                })
                raise e
                
        ConversableAgent.generate_reply = patched_generate_reply
    except ImportError:
        pass
