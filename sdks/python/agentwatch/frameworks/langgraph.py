import datetime
from ..client import AgentWatchClient

class LanggraphIntegration:
    def __init__(self, client: AgentWatchClient):
        self.client = client
        
    def setup(self):
        # Hook into langgraph callbacks
        pass
        
    def on_event(self, event_type, metadata):
        event = {
            'event_type': event_type,
            'framework': 'langgraph',
            'metadata': metadata,
            'started_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        self.client.send_event(event)
