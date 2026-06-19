import datetime
from ..client import AgentWatchClient

class LlamaindexIntegration:
    def __init__(self, client: AgentWatchClient):
        self.client = client
        
    def setup(self):
        # Hook into llamaindex callbacks
        pass
        
    def on_event(self, event_type, metadata):
        event = {
            'event_type': event_type,
            'framework': 'llamaindex',
            'metadata': metadata,
            'started_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        self.client.send_event(event)
