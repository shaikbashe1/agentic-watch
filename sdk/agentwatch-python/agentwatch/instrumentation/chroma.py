import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_chroma():
    try:
        import chromadb
    except ImportError:
        return
        
    def query_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("chromadb.Collection.query") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "chroma")
            span.set_attribute("db.operation", "query")

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                if result and "ids" in result:
                    span.set_attribute("db.retrieval_count", len(result["ids"][0]) if result["ids"] else 0)
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'chromadb.api.models.Collection',
            'Collection.query',
            query_wrapper
        )
    except AttributeError:
        pass
