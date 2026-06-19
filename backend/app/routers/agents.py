from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.agent import Agent, AgentHealthStatus
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/agents", tags=["agents"])

class AgentRegisterIn(BaseModel):
    name: str
    version: str
    framework: str
    description: str = ""
    owner_team: str = "default"
    tags: dict = {}
    environment: str = "production"
    workspace_id: str

@router.post("/register")
async def register_agent(agent_data: AgentRegisterIn, db: Session = Depends(get_db)):
    """Agents self-register on first run"""
    agent_id = str(uuid.uuid4())
    
    new_agent = Agent(
        id=agent_id,
        workspace_id=agent_data.workspace_id,
        name=agent_data.name,
        version=agent_data.version,
        framework=agent_data.framework,
        environment=agent_data.environment,
        tags=agent_data.tags,
        created_at=datetime.utcnow()
    )
    
    health_status = AgentHealthStatus(
        agent_id=agent_id,
        status="healthy",
        total_runs=0,
        success_rate=100.0
    )
    
    db.add(new_agent)
    db.add(health_status)
    db.commit()
    db.refresh(new_agent)
    
    return {"agent_id": new_agent.id, "status": "registered"}

@router.get("/")
async def list_agents(workspace_id: str, db: Session = Depends(get_db)):
    return db.query(Agent).filter(Agent.workspace_id == workspace_id).all()

@router.get("/{id}/health")
async def get_agent_health(id: str, db: Session = Depends(get_db)):
    health = db.query(AgentHealthStatus).filter(AgentHealthStatus.agent_id == id).first()
    if not health:
        raise HTTPException(status_code=404, detail="Agent health not found")
    return health
