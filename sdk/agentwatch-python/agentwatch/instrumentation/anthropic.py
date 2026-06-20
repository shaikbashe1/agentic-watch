import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_anthropic():
    import anthropic
    
    def messages_create_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("anthropic.messages.create") as span:
            span.set_attribute("agentwatch.span_type", "llm")
            span.set_attribute("llm.provider", "anthropic")
            
            model = kwargs.get("model", "unknown")
            span.set_attribute("llm.model", model)
            
            # Serialize prompts safely
            messages = kwargs.get("messages", [])
            span.set_attribute("llm.prompt", json.dumps(messages))

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                
                # Extract usage and response
                if hasattr(result, "usage") and result.usage:
                    span.set_attribute("llm.usage.prompt_tokens", result.usage.input_tokens)
                    span.set_attribute("llm.usage.completion_tokens", result.usage.output_tokens)
                    span.set_attribute("llm.usage.total_tokens", result.usage.input_tokens + result.usage.output_tokens)
                
                if hasattr(result, "content") and len(result.content) > 0:
                    span.set_attribute("llm.response", result.content[0].text)
                    
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    wrapt.wrap_function_wrapper(
        'anthropic.resources.messages',
        'Messages.create',
        messages_create_wrapper
    )
