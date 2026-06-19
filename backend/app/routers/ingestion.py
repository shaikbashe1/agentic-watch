from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime, timezone
import uuid
import logging

from ..database import get_db
from ..services.auth_service import get_workspace_from_api_key
from ..models.events import Event
from ..tasks.risk_scoring import evaluate_risk

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["ingestion"])

class BatchEventRequest(BaseModel):
    events: List[Dict[str, Any]]

@router.post("/batch", status_code=202)
async def ingest_batch(
    payload: BatchEventRequest, 
    workspace_id: str = Depends(get_workspace_from_api_key), 
    db: Session = Depends(get_db)
):
    event_ids_for_risk = []
    
    for event_data in payload.events:
        event_id = str(uuid.uuid4())
        
        # Parse basic fields
        db_event = Event(
            id=event_id,
            workspace_id=workspace_id,
            trace_id=event_data.get("trace_id", str(uuid.uuid4())),
            span_id=event_data.get("span_id", str(uuid.uuid4())),
            session_id=event_data.get("session_id", "unknown"),
            event_type=event_data.get("event_type", "unknown"),
            started_at=datetime.now(timezone.utc),
            latency_ms=event_data.get("latency_ms"),
            llm_provider=event_data.get("provider"),
            llm_model=event_data.get("model"),
            input_tokens=event_data.get("input_tokens"),
            output_tokens=event_data.get("output_tokens"),
            payload=event_data.get("payload", {})
        )
        db.add(db_event)
        event_ids_for_risk.append(event_id)
        
    db.commit()
    
    # Trigger asynchronous risk evaluation for LLM calls
    for e_id in event_ids_for_risk:
        try:
            evaluate_risk.delay(e_id)
        except Exception as e:
            logger.warning(f"Celery failed, skipping async evaluation: {e}")
        
    return {"status": "accepted", "ingested": len(payload.events)}
