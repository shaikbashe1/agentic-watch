import functools
import inspect
from opentelemetry import trace
from .telemetry import get_tracer

def _base_trace(span_type: str, name: str = None, **custom_attributes):
    """Base decorator for all trace types."""
    def decorator(func):
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            tracer = get_tracer()
            span_name = name or func.__name__
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("agentwatch.span_type", span_type)
                for k, v in custom_attributes.items():
                    span.set_attribute(k, v)
                
                try:
                    result = func(*args, **kwargs)
                    span.set_status(trace.StatusCode.OK)
                    return result
                except Exception as e:
                    span.set_status(trace.StatusCode.ERROR, str(e))
                    span.record_exception(e)
                    raise

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            tracer = get_tracer()
            span_name = name or func.__name__
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("agentwatch.span_type", span_type)
                for k, v in custom_attributes.items():
                    span.set_attribute(k, v)
                
                try:
                    result = await func(*args, **kwargs)
                    span.set_status(trace.StatusCode.OK)
                    return result
                except Exception as e:
                    span.set_status(trace.StatusCode.ERROR, str(e))
                    span.record_exception(e)
                    raise

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator

def trace_agent(name: str = None, **kwargs):
    return _base_trace("agent", name, **kwargs)

def trace_tool(name: str = None, **kwargs):
    return _base_trace("tool", name, **kwargs)

def trace_workflow(name: str = None, **kwargs):
    return _base_trace("workflow", name, **kwargs)

def trace_llm(name: str = None, **kwargs):
    return _base_trace("llm", name, **kwargs)

def trace_memory(name: str = None, **kwargs):
    return _base_trace("memory", name, **kwargs)

def trace_handoff(name: str = None, **kwargs):
    return _base_trace("handoff", name, **kwargs)

def trace_delegation(name: str = None, **kwargs):
    return _base_trace("delegation", name, **kwargs)
