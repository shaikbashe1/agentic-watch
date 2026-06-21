import random
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.models.agent import Agent as AgentModel
from app.models.log import TelemetryLog as LogModel

router = APIRouter()

class Metric(BaseModel):
    label: str
    value: str
    change: str
    trend: str

class Agent(BaseModel):
    name: str
    role: str
    status: str
    tokens: str

class LogEntry(BaseModel):
    timestamp: str
    agent: str
    message: str
    color: str

@router.get("/metrics", response_model=List[Metric])
async def get_metrics(db: Session = Depends(get_db)):
    # Calculate real log count to simulate activity
    total_logs = db.query(LogModel).count()
    base_tasks = 8400 + total_logs * 3
    
    return [
        {"label": "Active Agents", "value": str(db.query(AgentModel).count()), "change": "+2", "trend": "up"},
        {"label": "Tasks Processed (24h)", "value": f"{base_tasks:,}", "change": "+14%", "trend": "up"},
        {"label": "System Error Rate", "value": "0.04%", "change": "-0.01%", "trend": "down"},
    ]

@router.get("/agents", response_model=List[Agent])
async def get_agents(db: Session = Depends(get_db)):
    agents = db.query(AgentModel).all()
    return [
        {"name": a.name, "role": a.role, "status": a.status, "tokens": a.tokens} 
        for a in agents
    ]

@router.get("/logs", response_model=List[LogEntry])
async def get_logs(db: Session = Depends(get_db)):
    logs = db.query(LogModel).order_by(LogModel.id.desc()).limit(8).all()
    return [
        {"timestamp": l.timestamp, "agent": l.agent, "message": l.message, "color": l.color}
        for l in logs
    ]
