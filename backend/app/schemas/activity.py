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
    # When reading from ORM, SQLAlchemy puts the column value in `metadata_`.
    # The class-level `metadata` is the MetaData() object, so we must read `metadata_`.
    metadata_: Optional[Dict[str, Any]] = Field(
        default=None,
        validation_alias="metadata_",
        serialization_alias="metadata",
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
