from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from uuid import UUID

router = APIRouter()

class AgentEvent(BaseModel):
    id: UUID
    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    session_id: str
    event_type: str
    framework: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    latency_ms: Optional[int] = None
    workspace_id: str
    agent_id: Optional[str] = None
    agent_name: str
    payload: Optional[dict] = None

class BatchIngestRequest(BaseModel):
    events: List[AgentEvent]

@router.post("/event")
async def ingest_event(event: AgentEvent):
    # In a real app, this goes to Celery or TimescaleDB directly
    return {"status": "success", "event_id": str(event.id)}

@router.post("/batch")
async def ingest_batch(batch: BatchIngestRequest):
    # Convert Pydantic models to dicts for JSON serialization
    events_data = [evt.model_dump(mode='json') for evt in batch.events]
    
    # Enqueue to Redis for Celery worker to pick up
    from app.worker import ingest_batch_task
    ingest_batch_task.delay(events_data)
    
    return {"status": "enqueued", "events_queued": len(events_data)}
