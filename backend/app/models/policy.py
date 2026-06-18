from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from datetime import datetime
from ..database import Base


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    action_type = Column(String, index=True, nullable=False)
    decision = Column(String, nullable=False)  # allow, warn, block
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
