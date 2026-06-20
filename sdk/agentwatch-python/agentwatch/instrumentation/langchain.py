import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_langchain():
    try:
        from langchain_core.callbacks.base import BaseCallbackHandler
    except ImportError:
        return
        
    class AgentWatchCallbackHandler(BaseCallbackHandler):
        def __init__(self):
            self.tracer = get_tracer()
            self.current_span = None
            
        def on_chain_start(self, serialized, inputs, **kwargs):
            span = self.tracer.start_span("langchain.chain")
            span.set_attribute("agentwatch.span_type", "workflow")
            self.current_span = span

        def on_chain_end(self, outputs, **kwargs):
            if self.current_span:
                self.current_span.set_status(trace.StatusCode.OK)
                self.current_span.end()

        def on_chain_error(self, error, **kwargs):
            if self.current_span:
                self.current_span.set_status(trace.StatusCode.ERROR, str(error))
                self.current_span.record_exception(error)
                self.current_span.end()
