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

from ..core.risk_scorer import RiskScorer
from ..core.cost_calculator import CostCalculator
from ..core.alert_engine import AlertEngine
from ..models.alert import AlertRule
from ..models.webhooks import Webhook
from ..services.webhook_service import WebhookService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ingest", tags=["ingestion"])

risk_scorer = RiskScorer()
alert_engine = AlertEngine()

class BatchEventRequest(BaseModel):
    events: List[Dict[str, Any]]

@router.post("/batch", status_code=202)
async def ingest_batch(
    payload: BatchEventRequest, 
    background_tasks: BackgroundTasks,
    workspace_id: str = Depends(get_workspace_from_api_key), 
    db: Session = Depends(get_db)
):
    alert_rules = db.query(AlertRule).filter(AlertRule.workspace_id == workspace_id).all()
    active_webhooks = db.query(Webhook).filter(Webhook.workspace_id == workspace_id, Webhook.is_active == True).all()
    
    for event_data in payload.events:
        event_id = str(uuid.uuid4())
        
        # Risk Evaluation
        risk_result = risk_scorer.score_event(event_data)
        
        # Cost Calculation
        provider = event_data.get("llm_provider", event_data.get("provider"))
        model = event_data.get("llm_model", event_data.get("model"))
        input_tokens = event_data.get("input_tokens", 0) or 0
        output_tokens = event_data.get("output_tokens", 0) or 0
        
        cost = CostCalculator.calculate_cost(model, input_tokens, output_tokens) if model else 0.0
        
        db_event = Event(
            id=event_id,
            workspace_id=workspace_id,
            trace_id=event_data.get("trace_id", str(uuid.uuid4())),
            span_id=event_data.get("span_id", str(uuid.uuid4())),
            session_id=event_data.get("session_id", "unknown"),
            event_type=event_data.get("event_type", "unknown"),
            started_at=datetime.now(timezone.utc),
            latency_ms=event_data.get("latency_ms"),
            llm_provider=provider,
            llm_model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            risk_score=risk_result.score,
            payload=event_data.get("payload", {})
        )
        db.add(db_event)
        
        # Alert Evaluation
        alert_decisions = alert_engine.evaluate(alert_rules, {**event_data, "risk_score": risk_result.score, "cost": cost})
        
        # If any alert is triggered, or risk is extremely high, dispatch global webhooks
        if alert_decisions or risk_result.score >= 80:
            for decision in alert_decisions:
                alert_engine.dispatch(decision)
            
            if active_webhooks:
                # We do not pass db session to background tasks; instead we pass the fetched webhooks.
                background_tasks.add_task(
                    WebhookService.dispatch,
                    webhooks=active_webhooks,
                    event_type="policy_violation" if risk_result.score >= 80 else "alert_triggered",
                    payload=event_data
                )
                
    db.commit()
    
    return {"status": "accepted", "ingested": len(payload.events)}
