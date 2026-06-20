from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class ActivityBase(BaseModel):
    agent_name: str
    action_type: str
    action_description: str
    target_resource: str
    status: str
    metadata_: Optional[Dict[str, Any]] = Field(default=None, alias="metadata")


class ActivityCreate(ActivityBase):
    # Optional: provide user_goal to trigger inline alignment + alert generation
    user_goal: Optional[str] = Field(default=None, exclude=True)


class ActivityResponse(ActivityBase):
    id: int
    timestamp: datetime
    risk_score: Optional[float] = None
    alignment_score: Optional[float] = None
    policy_decision: Optional[str] = None
    # Read metadata_ from the ORM column (named metadata_ in Python)
    metadata_: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias="metadata_",
        serialization_alias="metadata",
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
