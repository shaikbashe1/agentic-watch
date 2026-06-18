from sqlalchemy import Column, Integer, String, JSON, DateTime, Float
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
    # Risk & alignment (populated when user_goal is provided on creation)
    risk_score = Column(Float, nullable=True)
    alignment_score = Column(Float, nullable=True)
    policy_decision = Column(String, nullable=True)  # allow / warn / block
