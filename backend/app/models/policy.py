from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid
from ..database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    workspace_id = Column(String, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    action = Column(String, nullable=False)  # BLOCK, REDACT, ALERT
    
    # conditions will store the JSON AST rule for the policy
    # e.g. {"field": "model", "operator": "==", "value": "gpt-4"}
    conditions = Column(JSONB, nullable=False)
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
