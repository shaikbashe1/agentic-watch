from sqlalchemy import Column, Integer, String, Float, DateTime
from ..database import Base
from datetime import datetime

class TokenUsage(Base):
    __tablename__ = "token_usage"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    prompt_tokens = Column(Integer)
    completion_tokens = Column(Integer)
    total_tokens = Column(Integer)
    cost_usd = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
