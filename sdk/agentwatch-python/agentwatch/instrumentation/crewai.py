import wrapt
from opentelemetry import trace
from agentwatch.telemetry import get_tracer

def instrument_crewai():
    try:
        import crewai
    except ImportError:
        return
        
    def crew_kickoff_wrapper(wrapped, instance, args, kwargs):
        tracer = get_tracer()
        with tracer.start_as_current_span("crewai.Crew.kickoff") as span:
            span.set_attribute("agentwatch.span_type", "workflow")
            span.set_attribute("framework", "crewai")
            
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
            'crewai.crew',
            'Crew.kickoff',
            crew_kickoff_wrapper
        )
    except AttributeError:
        pass
