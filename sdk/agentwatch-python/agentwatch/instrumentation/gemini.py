import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_gemini():
    try:
        import google.generativeai as genai
    except ImportError:
        return
        
    def generate_content_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("google.generativeai.generate_content") as span:
            span.set_attribute("agentwatch.span_type", "llm")
            span.set_attribute("llm.provider", "gemini")
            
            # Extract prompt safely
            prompt = kwargs.get("contents", args[0] if args else "unknown")
            span.set_attribute("llm.prompt", str(prompt))

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                
                # Gemini usage metadata
                if hasattr(result, "usage_metadata"):
                    span.set_attribute("llm.usage.prompt_tokens", result.usage_metadata.prompt_token_count)
                    span.set_attribute("llm.usage.completion_tokens", result.usage_metadata.candidates_token_count)
                    span.set_attribute("llm.usage.total_tokens", result.usage_metadata.total_token_count)
                
                if hasattr(result, "text"):
                    span.set_attribute("llm.response", result.text)
                    
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    try:
        wrapt.wrap_function_wrapper(
            'google.generativeai.generative_models.GenerativeModel',
            'generate_content',
            generate_content_wrapper
        )
    except AttributeError:
        pass
