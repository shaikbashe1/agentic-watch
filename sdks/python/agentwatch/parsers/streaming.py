import time
import json

class SSEStreamingParser:
    """
    Parses Server-Sent Events (SSE) from LLM providers to reconstruct chunks,
    measure Time-To-First-Token (TTFT), and calculate tokens per second.
    """
    
    def __init__(self):
        self.buffer = ""
        self.ttft = None
        self.start_time = time.time()
        
    def process_chunk(self, chunk_text: str):
        if not self.ttft:
            self.ttft = int((time.time() - self.start_time) * 1000)
            
        # Very basic accumulation for reconstruction
        self.buffer += chunk_text
        
    def get_metrics(self):
        duration = time.time() - self.start_time
        # Approximation of tokens if exact count isn't sent in last chunk
        approx_tokens = len(self.buffer) // 4
        
        tps = approx_tokens / duration if duration > 0 else 0
        
        return {
            "time_to_first_token_ms": self.ttft,
            "total_duration_ms": int(duration * 1000),
            "approximate_tokens": approx_tokens,
            "tokens_per_second": round(tps, 2)
        }
