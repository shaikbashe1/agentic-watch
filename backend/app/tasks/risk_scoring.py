from celery import shared_task
import logging
from ..database import SessionLocal
from ..models.events import Event
from .alerting import dispatch_webhooks

logger = logging.getLogger(__name__)

# Very simple heuristics for Phase 3 placeholder
HIGH_RISK_KEYWORDS = ["ignore all previous instructions", "system prompt", "bypass", "password", "secret", "credit card"]
MEDIUM_RISK_KEYWORDS = ["confidential", "internal only"]

@shared_task(name="app.tasks.risk_scoring.evaluate_risk")
def evaluate_risk(event_id: str):
    logger.info(f"Evaluating risk for event {event_id}")
    db = SessionLocal()
    try:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event or not event.payload:
            return
            
        risk_score = 0
        payload_str = str(event.payload).lower()
        
        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in payload_str:
                risk_score = max(risk_score, 90)
                
        for keyword in MEDIUM_RISK_KEYWORDS:
            if keyword in payload_str:
                risk_score = max(risk_score, 50)
                
        if risk_score > 0:
            event.risk_score = risk_score
            db.commit()
            
            if risk_score >= 80:
                # Trigger alerting asynchronously
                dispatch_webhooks.delay(event.workspace_id, event.id, risk_score)
                
    except Exception as e:
        logger.error(f"Error evaluating risk for event {event_id}: {e}")
    finally:
        db.close()
