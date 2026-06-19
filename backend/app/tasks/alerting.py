from celery import shared_task
import logging
import requests
from ..database import SessionLocal
from ..models.webhooks import Webhook

logger = logging.getLogger(__name__)

@shared_task(name="app.tasks.alerting.dispatch_webhooks")
def dispatch_webhooks(workspace_id: str, event_id: str, risk_score: int):
    logger.info(f"Dispatching webhooks for workspace {workspace_id}, event {event_id} with score {risk_score}")
    db = SessionLocal()
    try:
        webhooks = db.query(Webhook).filter(
            Webhook.workspace_id == workspace_id,
            Webhook.is_active == True
        ).all()
        
        payload = {
            "event": "risk.high",
            "data": {
                "event_id": event_id,
                "risk_score": risk_score,
                "workspace_id": workspace_id
            }
        }
        
        for webhook in webhooks:
            try:
                # In production, we'd sign the payload with webhook.secret
                requests.post(webhook.url, json=payload, timeout=5)
            except Exception as e:
                logger.warning(f"Failed to dispatch to webhook {webhook.url}: {e}")
                
    except Exception as e:
        logger.error(f"Error dispatching webhooks: {e}")
    finally:
        db.close()
