from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from ..database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, index=True)
    action_type = Column(String, index=True)
    action_description = Column(String)
    target_resource = Column(String)
    status = Column(String)
    metadata_ = Column("metadata", JSON, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
