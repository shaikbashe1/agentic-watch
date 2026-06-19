import uuid
import time
import functools

def patch_crewai(client):
    try:
        from crewai import Agent, Task, Crew
        from crewai.tools.tool_calling import ToolCalling
        
        # Patch Agent.execute_task
        original_execute_task = Agent.execute_task
        
        @functools.wraps(original_execute_task)
        def patched_execute_task(self, *args, **kwargs):
            start_time = time.time()
            trace_id = str(uuid.uuid4())
            span_id = str(uuid.uuid4())
            
            client.send_event({
                "trace_id": trace_id,
                "span_id": span_id,
                "event_type": "agent_start",
                "framework": "crewai",
                "agent_name": self.role,
                "payload": {"goal": self.goal}
            })
            
            try:
                result = original_execute_task(self, *args, **kwargs)
                latency = int((time.time() - start_time) * 1000)
                
                client.send_event({
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "event_type": "agent_end",
                    "framework": "crewai",
                    "agent_name": self.role,
                    "latency_ms": latency,
                    "payload": {"result": str(result)}
                })
                return result
            except Exception as e:
                latency = int((time.time() - start_time) * 1000)
                client.send_event({
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "event_type": "error",
                    "framework": "crewai",
                    "agent_name": self.role,
                    "latency_ms": latency,
                    "error": str(e)
                })
                raise e
                
        Agent.execute_task = patched_execute_task
        
    except ImportError:
        pass
