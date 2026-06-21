from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    status = Column(String, default="Offline")
    tokens = Column(String, default="0.0k")
