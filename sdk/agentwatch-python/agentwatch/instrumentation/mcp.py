import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_mcp():
    try:
        import mcp
    except ImportError:
        return
        
    def call_tool_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("mcp.call_tool") as span:
            span.set_attribute("agentwatch.span_type", "mcp")
            
            tool_name = kwargs.get("name", args[0] if args else "unknown")
            span.set_attribute("mcp.tool.name", tool_name)
            
            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    def read_resource_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("mcp.read_resource") as span:
            span.set_attribute("agentwatch.span_type", "mcp")
            
            uri = kwargs.get("uri", args[0] if args else "unknown")
            span.set_attribute("mcp.resource.uri", uri)
            
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
            'mcp',
            'ClientSession.call_tool',
            call_tool_wrapper
        )
        wrapt.wrap_function_wrapper(
            'mcp',
            'ClientSession.read_resource',
            read_resource_wrapper
        )
    except AttributeError:
        # If mcp structure changes
        pass
