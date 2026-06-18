import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.policy import Policy
from ..schemas.policy import PolicyCreate, PolicyUpdate, PolicyEvaluationResponse

logger = logging.getLogger(__name__)


def create_policy(db: Session, policy: PolicyCreate) -> Policy:
    existing = db.query(Policy).filter(Policy.name == policy.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Policy with name '{policy.name}' already exists")
    db_policy = Policy(
        name=policy.name,
        description=policy.description,
        action_type=policy.action_type,
        decision=policy.decision.value,
        is_active=policy.is_active,
    )
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    logger.info(f"Created policy id={db_policy.id} name={db_policy.name}")
    return db_policy


def get_policies(db: Session, skip: int = 0, limit: int = 100) -> list[Policy]:
    return db.query(Policy).offset(skip).limit(limit).all()


def get_policy(db: Session, policy_id: int) -> Policy:
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    return policy


def update_policy(db: Session, policy_id: int, policy_update: PolicyUpdate) -> Policy:
    policy = get_policy(db, policy_id)
    update_data = policy_update.model_dump(exclude_unset=True)
    if "decision" in update_data and update_data["decision"] is not None:
        update_data["decision"] = update_data["decision"].value if hasattr(update_data["decision"], "value") else update_data["decision"]
    for field, value in update_data.items():
        setattr(policy, field, value)
    from datetime import datetime
    policy.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(policy)
    logger.info(f"Updated policy id={policy_id}")
    return policy


def delete_policy(db: Session, policy_id: int) -> dict:
    policy = get_policy(db, policy_id)
    db.delete(policy)
    db.commit()
    logger.info(f"Deleted policy id={policy_id}")
    return {"message": "Policy deleted successfully"}


def evaluate_action(db: Session, action_type: str) -> PolicyEvaluationResponse:
    """Evaluate an action_type against active policies. Returns first matching policy decision."""
    policy = (
        db.query(Policy)
        .filter(Policy.action_type == action_type, Policy.is_active == True)
        .order_by(Policy.id)
        .first()
    )
    if policy:
        logger.info(f"Policy evaluation: action={action_type} decision={policy.decision} policy={policy.name}")
        return PolicyEvaluationResponse(decision=policy.decision, matched_policy=policy.name)
    # Default: allow if no policy matches
    return PolicyEvaluationResponse(decision="allow", matched_policy=None)
