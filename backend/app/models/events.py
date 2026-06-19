from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import JSON
from sqlalchemy.ext.declarative import declarative_base
from ..database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    workspace_id = Column(String, index=True, nullable=False)
    trace_id = Column(String, index=True, nullable=False)
    span_id = Column(String, nullable=False)
    parent_span_id = Column(String, nullable=True)
    session_id = Column(String, index=True, nullable=False)
    agent_id = Column(String, nullable=True)
    
    event_type = Column(String, nullable=False)
    framework = Column(String, nullable=True)
    
    started_at = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    latency_ms = Column(Integer, nullable=True)
    
    llm_provider = Column(String, nullable=True)
    llm_model = Column(String, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    cost_usd = Column(Float, nullable=True)
    
    tool_name = Column(String, nullable=True)
    risk_score = Column(Integer, nullable=True)
    policy_decision = Column(String, nullable=True)
    error = Column(String, nullable=True)
    
    payload = Column(JSON, nullable=True)
