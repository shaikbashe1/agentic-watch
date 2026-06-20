from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Execution Timeline
class TimelineEventBase(BaseModel):
    agent_id: str
    step_type: str
    status: str
    duration_ms: float

class TimelineEventCreate(TimelineEventBase):
    pass

class TimelineEventOut(TimelineEventBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Tool Traces
class ToolTraceBase(BaseModel):
    agent_id: str
    tool_name: str
    input_data: str
    output_data: str
    latency_ms: float
    success: bool

class ToolTraceCreate(ToolTraceBase):
    pass

class ToolTraceOut(ToolTraceBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Metrics
class TokenUsageBase(BaseModel):
    agent_id: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost_usd: float

class TokenUsageCreate(TokenUsageBase):
    pass

class TokenUsageOut(TokenUsageBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

# Workflows
class WorkflowExecutionBase(BaseModel):
    agent_id: str
    user_request: str
    flow_data: str
    status: str

class WorkflowExecutionCreate(WorkflowExecutionBase):
    pass

class WorkflowExecutionOut(WorkflowExecutionBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class VerificationResultBase(BaseModel):
    agent_id: str
    goal: str
    final_output: str
    success_score: float
    goal_completion_score: float
    result: str

class VerificationResultCreate(VerificationResultBase):
    pass

class VerificationResultOut(VerificationResultBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
