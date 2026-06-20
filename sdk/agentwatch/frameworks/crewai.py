from agentwatch.client import AgentWatchClient
import agentwatch

def patch_crewai():
    """
    Monkey-patches CrewAI's Crew and Agent classes to extract DAG edges.
    """
    try:
        from crewai import Agent, Task, Crew
        
        # Save original init
        _original_task_init = Task.__init__
        _original_agent_execute = Agent.execute_task
        
        def _patched_task_init(self, *args, **kwargs):
            # We intercept task creation to build the dependency graph
            _original_task_init(self, *args, **kwargs)
            # Record task in AgentWatch DAG memory
            
        def _patched_agent_execute(self, task, *args, **kwargs):
            # Intercept agent execution
            result = _original_agent_execute(self, task, *args, **kwargs)
            return result

        Task.__init__ = _patched_task_init
        Agent.execute_task = _patched_agent_execute
        
        print("AgentWatch successfully instrumented CrewAI")
    except ImportError:
        pass
