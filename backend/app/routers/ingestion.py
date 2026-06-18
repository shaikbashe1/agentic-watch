from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..services.auth_service import get_company_from_api_key
from ..models import execution, tool_trace, metrics, workflow, agent, tenant
from ..schemas import observability as obs_schemas
from ..services.ws_service import manager

router = APIRouter()

@router.post("/agents/register", tags=["ingestion"])
async def register_agent(payload: Dict[str, Any], company_id: str = Depends(get_company_from_api_key), db: Session = Depends(get_db)):
    import uuid
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    api_key_str = f"ak_{uuid.uuid4().hex}"
    
    # Create Agent
    db_agent = agent.Agent(
        id=agent_id,
        company_id=company_id,
        name=payload.get("name", "Unnamed Agent"),
        framework=payload.get("framework", "Custom"),
        description=payload.get("description", "")
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

@router.post("/telemetry", tags=["ingestion"])
async def ingest_telemetry(payload: Dict[str, Any], company_id: str = Depends(get_company_from_api_key), db: Session = Depends(get_db)):
    event_type = payload.get("event_type")
    agent_id = payload.get("agent_id")
    
    # Update agent health status
    if agent_id:
        db_agent = db.query(agent.Agent).filter(agent.Agent.id == agent_id).first()
        if db_agent and db_agent.status != "Connected":
            db_agent.status = "Connected"
            db.commit()

    if event_type == "timeline_step":
        event = obs_schemas.TimelineEventCreate(**payload)
        db_event = execution.TimelineEvent(**event.dict(), company_id=company_id)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        await manager.broadcast({"type": "TIMELINE_EVENT", "data": obs_schemas.TimelineEventOut.from_orm(db_event).dict(), "company_id": company_id})
        return {"status": "success", "id": db_event.id}
        
    elif event_type == "tool_call":
        trace = obs_schemas.ToolTraceCreate(**payload)
        db_trace = tool_trace.ToolTrace(**trace.dict(), company_id=company_id)
        db.add(db_trace)
        db.commit()
        db.refresh(db_trace)
        await manager.broadcast({"type": "TOOL_TRACE", "data": obs_schemas.ToolTraceOut.from_orm(db_trace).dict(), "company_id": company_id})
        return {"status": "success", "id": db_trace.id}
        
    elif event_type == "token_usage":
        usage = obs_schemas.TokenUsageCreate(**payload)
        db_usage = metrics.TokenUsage(**usage.dict(), company_id=company_id)
        db.add(db_usage)
        db.commit()
        db.refresh(db_usage)
        await manager.broadcast({"type": "TOKEN_USAGE", "data": obs_schemas.TokenUsageOut.from_orm(db_usage).dict(), "company_id": company_id})
        return {"status": "success", "id": db_usage.id}

    raise HTTPException(status_code=400, detail="Invalid event_type")
