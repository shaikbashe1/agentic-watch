from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import execution, tool_trace, metrics, workflow
from ..schemas import observability as obs_schemas
from ..services.ws_service import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Simple keep-alive or client messages
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Timeline
@router.post("/timeline", response_model=obs_schemas.TimelineEventOut, tags=["observability"])
async def create_timeline_event(event: obs_schemas.TimelineEventCreate, db: Session = Depends(get_db)):
    db_event = execution.TimelineEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    await manager.broadcast({"type": "TIMELINE_EVENT", "data": obs_schemas.TimelineEventOut.from_orm(db_event).dict()})
    return db_event

@router.get("/timeline/{agent_id}", response_model=List[obs_schemas.TimelineEventOut], tags=["observability"])
def get_timeline(agent_id: str, db: Session = Depends(get_db)):
    return db.query(execution.TimelineEvent).filter(execution.TimelineEvent.agent_id == agent_id).order_by(execution.TimelineEvent.timestamp.desc()).all()

# Tool Traces
@router.post("/tool-traces", response_model=obs_schemas.ToolTraceOut, tags=["observability"])
async def create_tool_trace(trace: obs_schemas.ToolTraceCreate, db: Session = Depends(get_db)):
    db_trace = tool_trace.ToolTrace(**trace.dict())
    db.add(db_trace)
    db.commit()
    db.refresh(db_trace)
    await manager.broadcast({"type": "TOOL_TRACE", "data": obs_schemas.ToolTraceOut.from_orm(db_trace).dict()})
    return db_trace

@router.get("/tool-traces", response_model=List[obs_schemas.ToolTraceOut], tags=["observability"])
def get_tool_traces(db: Session = Depends(get_db)):
    return db.query(tool_trace.ToolTrace).order_by(tool_trace.ToolTrace.timestamp.desc()).limit(100).all()

# Metrics
@router.post("/metrics/tokens", response_model=obs_schemas.TokenUsageOut, tags=["observability"])
async def create_token_usage(usage: obs_schemas.TokenUsageCreate, db: Session = Depends(get_db)):
    db_usage = metrics.TokenUsage(**usage.dict())
    db.add(db_usage)
    db.commit()
    db.refresh(db_usage)
    await manager.broadcast({"type": "TOKEN_USAGE", "data": obs_schemas.TokenUsageOut.from_orm(db_usage).dict()})
    return db_usage

@router.get("/metrics/tokens", response_model=List[obs_schemas.TokenUsageOut], tags=["observability"])
def get_token_usage(db: Session = Depends(get_db)):
    return db.query(metrics.TokenUsage).order_by(metrics.TokenUsage.timestamp.desc()).limit(100).all()

# Workflows
@router.post("/workflows", response_model=obs_schemas.WorkflowExecutionOut, tags=["observability"])
async def create_workflow(wf: obs_schemas.WorkflowExecutionCreate, db: Session = Depends(get_db)):
    db_wf = workflow.WorkflowExecution(**wf.dict())
    db.add(db_wf)
    db.commit()
    db.refresh(db_wf)
    await manager.broadcast({"type": "WORKFLOW", "data": obs_schemas.WorkflowExecutionOut.from_orm(db_wf).dict()})
    return db_wf

@router.get("/workflows", response_model=List[obs_schemas.WorkflowExecutionOut], tags=["observability"])
def get_workflows(db: Session = Depends(get_db)):
    return db.query(workflow.WorkflowExecution).order_by(workflow.WorkflowExecution.timestamp.desc()).limit(100).all()

@router.post("/verifications", response_model=obs_schemas.VerificationResultOut, tags=["observability"])
async def create_verification(ver: obs_schemas.VerificationResultCreate, db: Session = Depends(get_db)):
    db_ver = workflow.VerificationResult(**ver.dict())
    db.add(db_ver)
    db.commit()
    db.refresh(db_ver)
    await manager.broadcast({"type": "VERIFICATION", "data": obs_schemas.VerificationResultOut.from_orm(db_ver).dict()})
    return db_ver

@router.get("/verifications", response_model=List[obs_schemas.VerificationResultOut], tags=["observability"])
def get_verifications(db: Session = Depends(get_db)):
    return db.query(workflow.VerificationResult).order_by(workflow.VerificationResult.timestamp.desc()).limit(100).all()
