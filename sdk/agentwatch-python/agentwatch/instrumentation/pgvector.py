import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_pgvector():
    try:
        import psycopg2
    except ImportError:
        return
        
    def execute_wrapper(wrapped, instance, args, kwargs):
        query = args[0] if args else kwargs.get("query", "")
        
        # Only trace if it looks like a pgvector similarity search
        if "<->" in query or "<#>" in query or "<=>" in query:
            tracer = get_tracer()
            with tracer.start_as_current_span("psycopg2.cursor.execute_vector") as span:
                span.set_attribute("agentwatch.span_type", "memory")
                span.set_attribute("db.system", "postgresql")
                span.set_attribute("db.operation", "vector_search")
                
                try:
                    result = wrapped(*args, **kwargs)
                    span.set_status(trace.StatusCode.OK)
                    return result
                except Exception as e:
                    span.set_status(trace.StatusCode.ERROR, str(e))
                    span.record_exception(e)
                    raise
        else:
            return wrapped(*args, **kwargs)

    try:
        wrapt.wrap_function_wrapper(
            'psycopg2.extensions',
            'cursor.execute',
            execute_wrapper
        )
    except AttributeError:
        pass
