from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from ..database import Base
from datetime import datetime

class WorkflowExecution(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    agent_id = Column(String, index=True)
    user_request = Column(String)
    flow_data = Column(String) # JSON payload of graph nodes
    status = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    agent_id = Column(String, index=True)
    goal = Column(String)
    final_output = Column(String)
    success_score = Column(Float)
    goal_completion_score = Column(Float)
    result = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
