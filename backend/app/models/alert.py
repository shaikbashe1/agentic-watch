from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from ..database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    source = Column(String, nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=True)
    status = Column(String, default="open", nullable=False)  # open, acknowledged, resolved
    created_at = Column(DateTime, default=datetime.utcnow)
