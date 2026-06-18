from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from typing import Dict, Any

from ..database import get_db
from ..models import tenant, agent
from ..services.auth_service import get_current_user

router = APIRouter()

class AgentRegisterRequest(BaseModel):
    name: str
    framework: str
    description: str = ""

@router.post("/agents/register", tags=["keys"])
async def register_agent(payload: AgentRegisterRequest, current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = current_user.company_id
    
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    api_key_str = f"ak_{uuid.uuid4().hex}"
    
    # Create Agent
    db_agent = agent.Agent(
        id=agent_id,
        company_id=company_id,
        name=payload.name,
        framework=payload.framework,
        description=payload.description
    )
    db.add(db_agent)
    
    # Create API Key for this agent
    db_key = tenant.APIKey(
        id=f"key_{uuid.uuid4().hex[:8]}",
        company_id=company_id,
        agent_id=agent_id,
        key_hash=api_key_str, # in real app, hash this
        name=f"Key for {db_agent.name}"
    )
    db.add(db_key)
    
    db.commit()
    return {"agent_id": agent_id, "api_key": api_key_str}

@router.get("/api-keys", tags=["keys"])
async def get_api_keys(current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    keys = db.query(tenant.APIKey).filter(tenant.APIKey.company_id == current_user.company_id).all()
    return [{"id": k.id, "name": k.name, "key": k.key_hash, "active": k.is_active, "created_at": k.created_at} for k in keys]

@router.delete("/api-keys/{key_id}", tags=["keys"])
async def revoke_api_key(key_id: str, current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    key = db.query(tenant.APIKey).filter(tenant.APIKey.id == key_id, tenant.APIKey.company_id == current_user.company_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
        
    key.is_active = False
    db.commit()
    return {"status": "success"}
