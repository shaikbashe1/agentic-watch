from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from ..database import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    workspace_id = Column(String, index=True)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    framework = Column(String, nullable=True)
    environment = Column(String, nullable=True)
    tags = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_seen_at = Column(DateTime(timezone=True), nullable=True)

class AgentHealthStatus(Base):
    __tablename__ = "agent_health"
    
    agent_id = Column(String, primary_key=True, index=True)
    status = Column(String) # healthy, degraded, down, unknown
    total_runs = Column(Integer, default=0)
    success_rate = Column(Float, default=100.0)
    avg_latency_ms = Column(Integer, default=0)
    avg_cost_usd = Column(Float, default=0.0)
    avg_risk_score = Column(Float, default=0.0)
    last_seen = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_error = Column(String, nullable=True)
    active_sessions = Column(Integer, default=0)
