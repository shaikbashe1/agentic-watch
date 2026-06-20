import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_weaviate():
    try:
        import weaviate
    except ImportError:
        return
        
    def query_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("weaviate.query") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "weaviate")
            span.set_attribute("db.operation", "query")

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
            'weaviate.graphql.get',
            'GetBuilder.do',
            query_wrapper
        )
    except AttributeError:
        pass
