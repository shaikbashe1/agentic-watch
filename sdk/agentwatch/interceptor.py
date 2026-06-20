import httpcore
import json
from datetime import datetime
from typing import Optional
from .parsers.base import LLMEvent
from .parsers.openai import OpenAIParser
from .parsers.anthropic import AnthropicParser
from .client import AgentWatchClient

_original_handle = httpcore.HTTPConnection.handle_request

PARSERS = [
    OpenAIParser(),
    AnthropicParser()
]

def _patched_handle(self, request):
    start_time = datetime.utcnow()
    
    # Let the actual request go through
    response = _original_handle(self, request)
    
    end_time = datetime.utcnow()
    latency_ms = int((end_time - start_time).total_seconds() * 1000)

    try:
        # Check if any parser can handle this request URL
        for parser in PARSERS:
            if parser.can_handle(request):
                event = parser.parse(request, response, start_time, end_time, latency_ms)
                if event:
                    AgentWatchClient.get_instance().enqueue_event(event)
                break
    except Exception as e:
        # Failsafe: never break the user's application due to telemetry error
        print(f"AgentWatch interception error: {e}")

    return response

def setup_interceptor():
    """Enable the httpcore monkey-patch."""
    httpcore.HTTPConnection.handle_request = _patched_handle
