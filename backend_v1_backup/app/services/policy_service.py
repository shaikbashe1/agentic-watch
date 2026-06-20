import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.policy import Policy
from ..schemas.policy import PolicyCreate, PolicyUpdate

logger = logging.getLogger(__name__)

def create_policy(db: Session, workspace_id: str, policy: PolicyCreate) -> Policy:
    existing = db.query(Policy).filter(Policy.workspace_id == workspace_id, Policy.name == policy.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Policy '{policy.name}' already exists in this workspace")
        
    db_policy = Policy(
        workspace_id=workspace_id,
        name=policy.name,
        description=policy.description,
        action=policy.action.value,
        conditions=policy.conditions,
        is_active=policy.is_active,
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    logger.info(f"Created policy id={db_policy.id} name={db_policy.name} for workspace={workspace_id}")
    return db_policy

def get_policies(db: Session, workspace_id: str, skip: int = 0, limit: int = 100) -> list[Policy]:
    return db.query(Policy).filter(Policy.workspace_id == workspace_id).offset(skip).limit(limit).all()

def get_policy(db: Session, workspace_id: str, policy_id: str) -> Policy:
    policy = db.query(Policy).filter(Policy.workspace_id == workspace_id, Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy

def update_policy(db: Session, workspace_id: str, policy_id: str, policy_update: PolicyUpdate) -> Policy:
    policy = get_policy(db, workspace_id, policy_id)
    update_data = policy_update.model_dump(exclude_unset=True)
    
    if "action" in update_data and update_data["action"] is not None:
        update_data["action"] = update_data["action"].value if hasattr(update_data["action"], "value") else update_data["action"]
        
    for field, value in update_data.items():
        setattr(policy, field, value)
        
    from datetime import datetime
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    return policy

def delete_policy(db: Session, workspace_id: str, policy_id: str) -> dict:
    policy = get_policy(db, workspace_id, policy_id)
    db.delete(policy)
    db.commit()
    return {"status": "success"}
