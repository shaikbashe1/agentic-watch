import os
import uuid
from .client import AgentWatchClient
from .interceptor import patch_all

_global_client = None

def init(api_key: str = None, api_url: str = None, environment: str = "production", tags: dict = None):
    """
    Initialize AgentWatch to intercept all LLM calls.
    """
    global _global_client
    
    api_key = api_key or os.environ.get("AGENTWATCH_API_KEY")
    api_url = api_url or os.environ.get("AGENTWATCH_API_URL", "http://localhost:8000")
    
    if not api_key:
        raise ValueError("AgentWatch requires an API Key.")
        
    session_id = str(uuid.uuid4())
    _global_client = AgentWatchClient(api_key, api_url, session_id, environment, tags or {})
    
    # Patch all supported HTTP clients
    patch_all(_global_client)
    return _global_client

def get_client():
    return _global_client
