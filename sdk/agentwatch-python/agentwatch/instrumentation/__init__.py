import logging
from .openai import instrument_openai
from .anthropic import instrument_anthropic

logger = logging.getLogger(__name__)

def instrument_all():
    """Auto-instruments all supported libraries if they are installed."""
    try:
        instrument_openai()
        logger.info("OpenAI instrumentation enabled.")
    except ImportError:
        pass

    try:
        instrument_anthropic()
        logger.info("Anthropic instrumentation enabled.")
    except ImportError:
        pass
    
    try:
        from .pinecone import instrument_pinecone
        instrument_pinecone()
        logger.info("Pinecone instrumentation enabled.")
    except ImportError:
        pass

    try:
        from .mcp import instrument_mcp
        instrument_mcp()
        logger.info("MCP instrumentation enabled.")
    except ImportError:
        pass

    # New LLMs
    for module_name in ['gemini', 'groq', 'bedrock', 'ollama']:
        try:
            mod = __import__(f"agentwatch.instrumentation.{module_name}", fromlist=[f"instrument_{module_name}"])
            getattr(mod, f"instrument_{module_name}")()
        except (ImportError, AttributeError):
            pass

    # New Frameworks
    for module_name in ['langchain', 'crewai']:
        try:
            mod = __import__(f"agentwatch.instrumentation.{module_name}", fromlist=[f"instrument_{module_name}"])
            getattr(mod, f"instrument_{module_name}")()
        except (ImportError, AttributeError):
            pass

    # New Vector DBs
    for module_name in ['weaviate', 'qdrant', 'chroma', 'lancedb', 'milvus', 'pgvector']:
        try:
            mod = __import__(f"agentwatch.instrumentation.{module_name}", fromlist=[f"instrument_{module_name}"])
            getattr(mod, f"instrument_{module_name}")()
        except (ImportError, AttributeError):
            pass
