import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_groq():
    try:
        import groq
    except ImportError:
        return
        
    def chat_completions_create_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("groq.chat.completions.create") as span:
            span.set_attribute("agentwatch.span_type", "llm")
            span.set_attribute("llm.provider", "groq")
            
            model = kwargs.get("model", "unknown")
            span.set_attribute("llm.model", model)
            
            messages = kwargs.get("messages", [])
            span.set_attribute("llm.prompt", json.dumps(messages))

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                
                if hasattr(result, "usage") and result.usage:
                    span.set_attribute("llm.usage.prompt_tokens", result.usage.prompt_tokens)
                    span.set_attribute("llm.usage.completion_tokens", result.usage.completion_tokens)
                    span.set_attribute("llm.usage.total_tokens", result.usage.total_tokens)
                
                if hasattr(result, "choices") and len(result.choices) > 0:
                    span.set_attribute("llm.response", result.choices[0].message.content)
                    
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'groq.resources.chat.completions',
            'Completions.create',
            chat_completions_create_wrapper
        )
    except AttributeError:
        pass
