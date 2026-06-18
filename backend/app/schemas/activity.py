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
    pass

class ActivityResponse(ActivityBase):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
