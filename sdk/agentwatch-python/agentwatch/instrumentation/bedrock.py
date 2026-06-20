import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_bedrock():
    try:
        import boto3
    except ImportError:
        return
        
    def invoke_model_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("boto3.bedrock.invoke_model") as span:
            span.set_attribute("agentwatch.span_type", "llm")
            span.set_attribute("llm.provider", "bedrock")
            
            modelId = kwargs.get("modelId", args[0] if args else "unknown")
            span.set_attribute("llm.model", modelId)
            
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
            'botocore.client',
            'BaseClient._make_api_call',
            invoke_model_wrapper
        )
    except AttributeError:
        pass
