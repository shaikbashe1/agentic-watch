import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer
import json

def instrument_pinecone():
    try:
        import pinecone
    except ImportError:
        return
        
    def query_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("pinecone.Index.query") as span:
            span.set_attribute("agentwatch.span_type", "memory")
            span.set_attribute("db.system", "pinecone")
            span.set_attribute("db.operation", "query")
            
            top_k = kwargs.get("top_k", 10)
            span.set_attribute("pinecone.top_k", top_k)

            try:
                result = wrapped(*args, **kwargs)
                span.set_status(trace.StatusCode.OK)
                
                # Extract recall and result count
                if hasattr(result, "matches"):
                    span.set_attribute("db.retrieval_count", len(result.matches))
                    
                return result
            except Exception as e:
                span.set_status(trace.StatusCode.ERROR, str(e))
                span.record_exception(e)
                raise

    wrapt.wrap_function_wrapper(
        'pinecone.data.index',
        'Index.query',
        query_wrapper
    )
