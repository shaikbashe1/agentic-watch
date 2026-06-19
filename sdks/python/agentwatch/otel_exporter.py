import logging
try:
    from opentelemetry import trace
    from opentelemetry.trace import Status, StatusCode
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    OTEL_AVAILABLE = True
except ImportError:
    OTEL_AVAILABLE = False

logger = logging.getLogger(__name__)

class AgentWatchOTELIntegration:
    def __init__(self, service_name: str, otlp_endpoint: str = None):
        self.service_name = service_name
        self.tracer = None
        self.otlp_endpoint = otlp_endpoint
        self._init_otel()

    def _init_otel(self):
        if not OTEL_AVAILABLE:
            logger.warning("opentelemetry packages not installed. OTEL export disabled.")
            return

        provider = TracerProvider()
        
        if self.otlp_endpoint:
            exporter = OTLPSpanExporter(endpoint=self.otlp_endpoint)
        else:
            # Default OTLP exporter if no endpoint provided (will use env vars like OTEL_EXPORTER_OTLP_ENDPOINT)
            exporter = OTLPSpanExporter()
            
        processor = BatchSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        
        self.tracer = trace.get_tracer(self.service_name)
        logger.info(f"OpenTelemetry integration initialized for {self.service_name}")

    def export_event(self, event_data: dict):
        """Convert AgentWatch event to an OTEL Span and export it"""
        if not self.tracer:
            return

        event_type = event_data.get("event_type", "unknown")
        span_name = f"{event_type}: {event_data.get('tool_name') or event_data.get('llm_model') or 'event'}"
        
        # Start a new span. In a real implementation we would link parent_span_id to build the distributed trace correctly.
        with self.tracer.start_as_current_span(span_name) as span:
            span.set_attribute("agentwatch.workspace_id", event_data.get("workspace_id", ""))
            span.set_attribute("agentwatch.session_id", event_data.get("session_id", ""))
            span.set_attribute("agentwatch.agent_name", event_data.get("agent_name", ""))
            
            if "cost_usd" in event_data and event_data["cost_usd"] is not None:
                span.set_attribute("agentwatch.cost_usd", event_data["cost_usd"])
                
            if "risk_score" in event_data and event_data["risk_score"] is not None:
                span.set_attribute("agentwatch.risk_score", event_data["risk_score"])
                
            if event_data.get("error"):
                span.set_status(Status(StatusCode.ERROR, event_data["error"]))
                span.record_exception(Exception(event_data["error"]))
            else:
                span.set_status(Status(StatusCode.OK))
