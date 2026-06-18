from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from ..database import Base
from datetime import datetime

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True, index=True)
    company_id = Column(String, ForeignKey("companies.id"))
    name = Column(String)
    framework = Column(String) # LangGraph, CrewAI, AutoGen, Custom
    description = Column(String, nullable=True)
    status = Column(String, default="Disconnected") # Connected, Disconnected, Error
    created_at = Column(DateTime, default=datetime.utcnow)
