from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from datetime import datetime, timedelta, timezone
from fastapi.responses import JSONResponse

from ..database import get_db
from ..services.auth_service import get_workspace_from_api_key
from ..models.events import Event

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/traces")
async def get_traces(
    limit: int = 50,
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    """Get all traces (unique trace_ids) for a workspace."""
    traces = db.query(Event.trace_id, func.min(Event.started_at).label("started_at"), func.sum(Event.cost_usd).label("total_cost"), func.max(Event.risk_score).label("max_risk")).filter(Event.workspace_id == workspace_id).group_by(Event.trace_id).order_by(func.min(Event.started_at).desc()).limit(limit).all()
    
    return [
        {
            "trace_id": t.trace_id,
            "started_at": t.started_at,
            "total_cost": t.total_cost,
            "max_risk": t.max_risk
        }
        for t in traces
    ]

@router.get("/traces/{trace_id}")
async def get_trace_details(
    trace_id: str,
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    """Get all spans/events for a specific trace_id (powers ReactFlow DAG)."""
    events = db.query(Event).filter(Event.workspace_id == workspace_id, Event.trace_id == trace_id).order_by(Event.started_at.asc()).all()
    
    return events

@router.get("/cost")
async def get_cost_analytics(
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    """Get cost metrics per provider and model."""
    costs = db.query(
        Event.llm_provider, 
        Event.llm_model, 
        func.sum(Event.cost_usd).label("total_cost")
    ).filter(Event.workspace_id == workspace_id).group_by(Event.llm_provider, Event.llm_model).all()
    
    return [{"provider": c.llm_provider, "model": c.llm_model, "total_cost": c.total_cost} for c in costs]

@router.get("/timeseries/tokens")
async def get_tokens_timeseries(
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    """Get total tokens used per day/hour (mock aggregation for SQLite compatibility)."""
    # SQLite doesn't have date_trunc, so we group in memory for simplicity on small datasets
    events = db.query(Event.started_at, Event.tokens_total).filter(Event.workspace_id == workspace_id, Event.tokens_total > 0).order_by(Event.started_at.desc()).limit(1000).all()
    
    # Group by date (YYYY-MM-DD)
    grouped = {}
    for ev in events:
        day = ev.started_at.strftime("%Y-%m-%d")
        grouped[day] = grouped.get(day, 0) + ev.tokens_total
        
    res = [{"date": k, "tokens": v} for k, v in grouped.items()]
    res.sort(key=lambda x: x["date"])
    return res

@router.get("/timeseries/costs")
async def get_costs_timeseries(
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    events = db.query(Event.started_at, Event.cost_usd).filter(Event.workspace_id == workspace_id, Event.cost_usd > 0).order_by(Event.started_at.desc()).limit(1000).all()
    grouped = {}
    for ev in events:
        day = ev.started_at.strftime("%Y-%m-%d")
        grouped[day] = grouped.get(day, 0.0) + ev.cost_usd
        
    res = [{"date": k, "cost": round(v, 4)} for k, v in grouped.items()]
    res.sort(key=lambda x: x["date"])
    return res

@router.get("/timeseries/latency")
async def get_latency_timeseries(
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    events = db.query(Event.started_at, Event.latency).filter(Event.workspace_id == workspace_id, Event.latency > 0).order_by(Event.started_at.desc()).limit(100).all()
    grouped = {}
    for ev in events:
        time_lbl = ev.started_at.strftime("%H:%M:%S")
        grouped[time_lbl] = grouped.get(time_lbl, 0.0) + ev.latency
        
    res = [{"time": k, "latency": round(v, 3)} for k, v in grouped.items()]
    res.sort(key=lambda x: x["time"])
    return res

@router.get("/reports/compliance")
async def generate_compliance_report(
    type: str = "soc2",
    workspace_id: str = Depends(get_workspace_from_api_key),
    db: Session = Depends(get_db)
):
    """Generate a mock compliance report (SOC2 / HIPAA)."""
    # In a real system, this would use ReportLab to generate a PDF.
    report = {
        "report_type": type.upper(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workspace_id": workspace_id,
        "status": "COMPLIANT",
        "checks": [
            {"name": "PII Redaction", "status": "PASS"},
            {"name": "Audit Logging", "status": "PASS"},
            {"name": "Access Controls", "status": "PASS"}
        ]
    }
    return JSONResponse(content=report)
