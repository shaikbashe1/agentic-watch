import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_milvus():
    try:
        import pymilvus
    except ImportError:
        return
        
    def search_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("pymilvus.Collection.search") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "milvus")
            span.set_attribute("db.operation", "search")

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                span.set_attribute("db.retrieval_count", len(result[0]) if result else 0)
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'pymilvus.client.collection',
            'Collection.search',
            search_wrapper
        )
    except AttributeError:
        pass
