from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database import Base
from datetime import datetime

class TimelineEvent(Base):
    __tablename__ = "timeline_events"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, index=True)
    agent_id = Column(String, index=True)
    step_type = Column(String)
    status = Column(String)
    duration_ms = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
