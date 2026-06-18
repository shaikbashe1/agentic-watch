from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..database import get_db
from ..services.auth_service import get_company_from_api_key
from ..models import execution, tool_trace, metrics, workflow, agent, tenant, alerts
from ..schemas import observability as obs_schemas
import logging
from ..websockets import manager
import uuid
import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/telemetry", tags=["ingestion"])
async def ingest_telemetry(payload: Dict[str, Any], company_id: str = Depends(get_company_from_api_key), db: Session = Depends(get_db)):
    event_type = payload.get("event_type")
    agent_id = payload.get("agent_id")
    
    if not event_type or not agent_id:
        raise HTTPException(status_code=400, detail="Missing event_type or agent_id")

    # 1. Update Agent Health Status
    db_agent = db.query(agent.Agent).filter(agent.Agent.id == agent_id, agent.Agent.company_id == company_id).first()
    if db_agent and db_agent.status != "Connected":
        db_agent.status = "Connected"
        # Optional: db_agent.last_active_at = datetime.datetime.utcnow()
        db.commit()

    # Broadcast event via WebSockets
    ws_payload = {
        "event_type": event_type,
        "agent_id": agent_id,
        "payload": payload,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    await manager.broadcast_to_company(company_id, ws_payload)

    if event_type == "timeline_step":
        event = obs_schemas.TimelineEventCreate(**payload)
        db_event = execution.TimelineEvent(**event.dict(), company_id=company_id)
        db.add(db_event)
        db.commit()
        return {"status": "success", "id": db_event.id}
        
    elif event_type == "tool_call":
        trace = obs_schemas.ToolTraceCreate(**payload)
        db_trace = tool_trace.ToolTrace(**trace.dict(), company_id=company_id)
        db.add(db_trace)
        db.commit()
        
        # --- Automated Anomaly Detection (Logic Loop) ---
        last_tools = db.query(tool_trace.ToolTrace)\
                       .filter(tool_trace.ToolTrace.agent_id == agent_id)\
                       .order_by(tool_trace.ToolTrace.timestamp.desc())\
                       .limit(5).all()
        
        if len(last_tools) == 5:
            # Check if all 5 are the exact same tool and exact same inputs
            if all(t.tool_name == trace.tool_name and t.inputs == trace.inputs for t in last_tools):
                # Trigger Loop Alert
                db_alert = alerts.Alert(
                    id=f"alert_{uuid.uuid4().hex[:8]}",
                    company_id=company_id,
                    agent_id=agent_id,
                    title="Logic Loop Detected",
                    severity="Critical",
                    status="Open",
                    description=f"Agent is repeatedly calling '{trace.tool_name}' with identical inputs."
                )
                db.add(db_alert)
                db.commit()
                await manager.broadcast_to_company(company_id, {
                    "event_type": "alert",
                    "payload": {"title": db_alert.title, "severity": db_alert.severity}
                })

        return {"status": "success", "id": db_trace.id}
        
    elif event_type == "token_usage":
        usage = obs_schemas.TokenUsageCreate(**payload)
        db_usage = metrics.TokenUsage(**usage.dict(), company_id=company_id)
        db.add(db_usage)
        db.commit()
        return {"status": "success", "id": db_usage.id}

    raise HTTPException(status_code=400, detail="Invalid event_type")
