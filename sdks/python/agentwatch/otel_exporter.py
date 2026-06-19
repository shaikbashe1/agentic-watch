import logging

class OTELExporter:
    """
    Exports AgentWatch events natively to an OpenTelemetry (OTLP) backend.
    """
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self._setup_exporter()
        
    def _setup_exporter(self):
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
            
            provider = TracerProvider()
            processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=self.endpoint))
            provider.add_span_processor(processor)
            
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer("agentwatch-sdk")
            self.enabled = True
        except ImportError:
            logging.warning("OpenTelemetry SDK not installed. Run `pip install opentelemetry-sdk opentelemetry-exporter-otlp` to enable OTEL export.")
            self.enabled = False

    def export(self, event: dict):
        if not self.enabled:
            return
            
        # Convert internal AgentWatch event to an OTEL Span
        with self.tracer.start_as_current_span(event.get("event_type", "unknown")) as span:
            span.set_attribute("agentwatch.trace_id", event.get("trace_id", ""))
            span.set_attribute("agentwatch.framework", event.get("framework", ""))
            
            # Map LLM attributes
            if "llm_provider" in event:
                span.set_attribute("llm.provider", event["llm_provider"])
            if "llm_model" in event:
                span.set_attribute("llm.model", event["llm_model"])
                
            # Map Tool attributes
            if "tool_name" in event:
                span.set_attribute("tool.name", event["tool_name"])
