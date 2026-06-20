import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_ollama():
    try:
        import ollama
    except ImportError:
        return
        
    def chat_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("ollama.chat") as span:
            span.set_attribute("agentwatch.span_type", "llm")
            span.set_attribute("llm.provider", "ollama")
            
            model = kwargs.get("model", args[0] if args else "unknown")
            span.set_attribute("llm.model", model)
            
            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                if isinstance(result, dict) and "message" in result:
                    span.set_attribute("llm.response", result["message"].get("content", ""))
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'ollama',
            'chat',
            chat_wrapper
        )
    except AttributeError:
        pass
