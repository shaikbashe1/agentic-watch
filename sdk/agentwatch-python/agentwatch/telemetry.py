import os
from typing import Dict, Any, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

_tracer_provider = None

def init(config: Optional[Dict[str, Any]] = None) -> Any:
    """Initialize OpenTelemetry tracer provider for AgentWatch."""
    global _tracer_provider
    if _tracer_provider is not None:
        return _tracer_provider

    config = config or {}
    service_name = config.get("service_name", os.getenv("OTEL_SERVICE_NAME", "agentwatch-service"))
    endpoint = config.get("endpoint", os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"))

    resource = Resource.create({
        "service.name": service_name,
        "telemetry.sdk.name": "agentwatch",
        "telemetry.sdk.language": "python",
        "telemetry.sdk.version": "2.0.0"
    })

    _tracer_provider = TracerProvider(resource=resource)
    
    # Configure OTLP Exporter
    otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
    span_processor = BatchSpanProcessor(otlp_exporter)
    _tracer_provider.add_span_processor(span_processor)

    # Add console exporter for local debugging
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter
    console_processor = BatchSpanProcessor(ConsoleSpanExporter())
    _tracer_provider.add_span_processor(console_processor)

    trace.set_tracer_provider(_tracer_provider)
    
    return _tracer_provider

def get_tracer(name: str = "agentwatch.sdk"):
    """Get an OpenTelemetry tracer."""
    return trace.get_tracer(name)
