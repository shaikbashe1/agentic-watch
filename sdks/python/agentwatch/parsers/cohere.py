import datetime
from .base import BaseParser

class CohereParser(BaseParser):
    def build_event(self, request, response, req_body, res_body, trace_id, span_id, latency):
        model = req_body.get('model', 'unknown')
        return {
            'trace_id': trace_id,
            'span_id': span_id,
            'event_type': 'llm_call',
            'llm_provider': 'cohere',
            'llm_model': model,
            'latency_ms': latency,
            'started_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        
    def build_error_event(self, request, error_msg, trace_id, span_id, latency):
        return {
            'trace_id': trace_id,
            'span_id': span_id,
            'event_type': 'error',
            'llm_provider': 'cohere',
            'error': error_msg,
            'latency_ms': latency,
            'started_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
