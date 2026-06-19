from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from ..database import Base
from datetime import datetime
import uuid

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    workspace_id = Column(String, index=True)
    actor_id = Column(String)
    actor_email = Column(String)
    action = Column(String, index=True) # e.g. "policy.created"
    resource_type = Column(String)
    resource_id = Column(String)
    changes = Column(JSON, default={})
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow, index=True)
