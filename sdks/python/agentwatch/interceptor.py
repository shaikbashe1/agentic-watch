import logging
from .parsers.openai import OpenAIParser
from .parsers.anthropic import AnthropicParser

from .parsers.gemini import GeminiParser
from .parsers.bedrock import BedrockParser

def patch_all(client):
    try:
        import httpcore
        _original_handle_request = httpcore.ConnectionPool.handle_request
        
        def patched_handle_request(self, request):
            url = str(request.url)
            
            # Select parser
            parser = None
            if "api.openai.com" in url:
                parser = OpenAIParser(client)
            elif "api.anthropic.com" in url:
                parser = AnthropicParser(client)
            elif "generativelanguage.googleapis.com" in url:
                parser = GeminiParser(client)
            elif "bedrock-runtime" in url:
                parser = BedrockParser(client)
                
            if not parser:
                return _original_handle_request(self, request)
                
            return parser.handle_request(_original_handle_request, self, request)
            
        httpcore.ConnectionPool.handle_request = patched_handle_request
        logging.info("AgentWatch: httpcore patched successfully.")
    except ImportError:
        logging.warning("AgentWatch: httpcore not found, cannot monkey-patch.")
