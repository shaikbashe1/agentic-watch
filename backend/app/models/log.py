from sqlalchemy import Column, Integer, String
from app.core.database import Base

class TelemetryLog(Base):
    __tablename__ = "telemetry_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, index=True)
    agent = Column(String, index=True)
    message = Column(String)
    color = Column(String)
