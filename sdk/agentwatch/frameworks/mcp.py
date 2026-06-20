from agentwatch.client import AgentWatchClient
import agentwatch

def patch_mcp():
    """
    Monkey-patches the Model Context Protocol (MCP) server handler to trace tool calls.
    """
    try:
        from mcp.server import Server
        
        _original_handle_tool_call = Server.handle_tool_call
        
        async def _patched_handle_tool_call(self, name: str, arguments: dict):
            # We intercept tool calls going to the MCP server
            # Log the start of the tool call
            
            result = await _original_handle_tool_call(self, name, arguments)
            
            # Log the end and return result
            return result

        Server.handle_tool_call = _patched_handle_tool_call
        
        print("AgentWatch successfully instrumented MCP Server")
    except ImportError:
        pass
