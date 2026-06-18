from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from ..database import Base
from datetime import datetime

class ToolTrace(Base):
    __tablename__ = "tool_traces"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    tool_name = Column(String, index=True)
    input_data = Column(String)
    output_data = Column(String)
    latency_ms = Column(Float)
    success = Column(Boolean)
    timestamp = Column(DateTime, default=datetime.utcnow)
