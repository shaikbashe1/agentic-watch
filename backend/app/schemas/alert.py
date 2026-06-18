from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class SeverityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class AlertStatusEnum(str, Enum):
    open = "open"
    acknowledged = "acknowledged"
    resolved = "resolved"


class AlertBase(BaseModel):
    title: str
    description: Optional[str] = None
    severity: SeverityEnum
    source: str
    activity_id: Optional[int] = None
    status: AlertStatusEnum = AlertStatusEnum.open


class AlertCreate(AlertBase):
    pass


class AlertUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[SeverityEnum] = None
    source: Optional[str] = None
    status: Optional[AlertStatusEnum] = None


class AlertResponse(AlertBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
