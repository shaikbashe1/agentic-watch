from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ActionEnum(str, Enum):
    BLOCK = "BLOCK"
    REDACT = "REDACT"
    ALERT = "ALERT"


class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    action: ActionEnum
    conditions: Dict[str, Any]
    is_active: bool = True


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    action: Optional[ActionEnum] = None
    conditions: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class PolicyResponse(PolicyBase):
    id: str
    workspace_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PolicyEvaluationRequest(BaseModel):
    workspace_id: str
    payload: Dict[str, Any]


class PolicyEvaluationResponse(BaseModel):
    action: str
    matched_policy_id: Optional[str] = None
    reason: Optional[str] = None
