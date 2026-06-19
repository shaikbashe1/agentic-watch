class AgentWatchException(Exception):
    pass

class AgentWatchPolicyViolation(AgentWatchException):
    pass

class AgentWatchRateLimitExceeded(AgentWatchException):
    pass
