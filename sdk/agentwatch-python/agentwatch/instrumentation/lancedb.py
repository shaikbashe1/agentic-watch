import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_lancedb():
    try:
        import lancedb
    except ImportError:
        return
        
    def search_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("lancedb.Table.search") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "lancedb")
            span.set_attribute("db.operation", "search")

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'lancedb.table',
            'Table.search',
            search_wrapper
        )
    except AttributeError:
        pass
