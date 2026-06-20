from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from datetime import datetime
import uuid
from ..database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(String, primary_key=True, default=generate_uuid, index=True)
    workspace_id = Column(String, ForeignKey("workspaces.id"), index=True, nullable=False)
    url = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
