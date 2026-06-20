from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional
from app.core.policy_engine import PolicyEngine

router = APIRouter()

class EvaluationRequest(BaseModel):
    workspace_id: str
    agent_id: Optional[str] = None
    event_type: str
    payload: Dict[str, Any]

class EvaluationResponse(BaseModel):
    decision: str  # "allow", "warn", "block"
    reason: str
    risk_score: int

@router.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_action(request: EvaluationRequest):
    """
    Synchronous endpoint called by the AgentWatch Guard before an LLM or Tool executes.
    Evaluates the payload against Workspace policies and calculates real-time risk.
    """
    decision, reason, risk_score = PolicyEngine.evaluate(
        payload=request.payload,
        workspace_id=request.workspace_id
    )
    
    # If blocked, the SDK will intercept this and raise an exception, preventing the action
    return EvaluationResponse(
        decision=decision,
        reason=reason,
        risk_score=risk_score
    )
