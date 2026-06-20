"""
AgentWatch Enterprise Python SDK
"""
from typing import Dict, Optional

class AgentWatchConfig:
    def __init__(self):
        self.api_key: Optional[str] = None
        self.workspace_id: Optional[str] = None
        self.environment: str = "development"
        self.agent_name: str = "default-agent"
        self.agent_version: str = "1.0.0"
        self.tags: Dict[str, str] = {}
        self.policy_enforcement: bool = False
        self.risk_threshold: int = 100
        self.flush_interval: int = 5
        self.batch_size: int = 100

_config = AgentWatchConfig()

def init(
    api_key: str,
    workspace_id: str,
    environment: str = "development",
    agent_name: str = "default-agent",
    agent_version: str = "1.0.0",
    tags: Optional[Dict[str, str]] = None,
    policy_enforcement: bool = False,
    risk_threshold: int = 100,
    flush_interval: int = 5,
    batch_size: int = 100,
):
    """
    Initialize the AgentWatch SDK.
    This will set up the universal HTTP interceptors and background workers.
    """
    _config.api_key = api_key
    _config.workspace_id = workspace_id
    _config.environment = environment
    _config.agent_name = agent_name
    _config.agent_version = agent_version
    _config.tags = tags or {}
    _config.policy_enforcement = policy_enforcement
    _config.risk_threshold = risk_threshold
    _config.flush_interval = flush_interval
    _config.batch_size = batch_size

    # Setup Universal HTTP Interceptor
    from .interceptor import setup_interceptor
    setup_interceptor()

    # Trigger initial client instance to start background thread
    from .client import AgentWatchClient
    AgentWatchClient.get_instance()

    print(f"AgentWatch SDK initialized for workspace {workspace_id}")
