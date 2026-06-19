from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from ..database import get_db
from ..models.webhooks import Webhook
from ..models.tenant import User
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

class WebhookCreate(BaseModel):
    url: str
    secret: str
    
class WebhookResponse(BaseModel):
    id: str
    url: str
    is_active: bool

@router.post("", response_model=WebhookResponse)
def create_webhook(payload: WebhookCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_webhook = Webhook(
        workspace_id=current_user.workspace_id,
        url=payload.url,
        secret=payload.secret
    )
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@router.get("", response_model=List[WebhookResponse])
def list_webhooks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Webhook).filter(Webhook.workspace_id == current_user.workspace_id).all()

@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    webhook = db.query(Webhook).filter(Webhook.id == webhook_id, Webhook.workspace_id == current_user.workspace_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
        
    db.delete(webhook)
    db.commit()
    return {"status": "success"}
