from pydantic import BaseModel

class AlignmentRequest(BaseModel):
    user_goal: str
    agent_action: str

class AlignmentResponse(BaseModel):
    safe: bool
    alignment_score: int
    risk_score: int
    reason: str
