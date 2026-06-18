from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class DecisionEnum(str, Enum):
    allow = "allow"
    warn = "warn"
    block = "block"


class PolicyBase(BaseModel):
    name: str
    description: Optional[str] = None
    action_type: str
    decision: DecisionEnum
    is_active: bool = True

    @field_validator("decision", mode="before")
    @classmethod
    def validate_decision(cls, v: str) -> str:
        allowed = {"allow", "warn", "block"}
        if str(v).lower() not in allowed:
            raise ValueError(f"decision must be one of {allowed}")
        return str(v).lower()


class PolicyCreate(PolicyBase):
    pass


class PolicyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    action_type: Optional[str] = None
    decision: Optional[DecisionEnum] = None
    is_active: Optional[bool] = None


class PolicyResponse(PolicyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PolicyEvaluationRequest(BaseModel):
    action_type: str


class PolicyEvaluationResponse(BaseModel):
    decision: str
    matched_policy: Optional[str] = None
