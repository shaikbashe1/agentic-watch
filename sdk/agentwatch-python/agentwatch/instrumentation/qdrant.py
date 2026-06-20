import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_qdrant():
    try:
        import qdrant_client
    except ImportError:
        return
        
    def search_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("qdrant.search") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "qdrant")
            span.set_attribute("db.operation", "search")
            
            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                span.set_attribute("db.retrieval_count", len(result) if isinstance(result, list) else 0)
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'qdrant_client.qdrant_client',
            'QdrantClient.search',
            search_wrapper
        )
    except AttributeError:
        pass
