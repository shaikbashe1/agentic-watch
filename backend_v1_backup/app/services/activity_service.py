import logging
from sqlalchemy.orm import Session
from ..models.activity import Activity
from ..schemas.activity import ActivityCreate
from ..schemas.alignment import AlignmentRequest
from fastapi import HTTPException
from . import policy_service, alert_service, alignment_service

logger = logging.getLogger(__name__)

# Threshold: risk_score >= this triggers a high-risk alert
HIGH_RISK_THRESHOLD = 70
# Threshold: alignment_score <= this triggers a goal-alignment failure alert
LOW_ALIGNMENT_THRESHOLD = 30


def create_activity(db: Session, activity: ActivityCreate) -> Activity:
    db_activity = Activity(
        agent_name=activity.agent_name,
        action_type=activity.action_type,
        action_description=activity.action_description,
        target_resource=activity.target_resource,
        status=activity.status,
        metadata_=activity.metadata_,
    )

    # Step 1: Goal alignment (if user_goal provided)
    if activity.user_goal:
        alignment_result = alignment_service.evaluate_alignment(
            AlignmentRequest(user_goal=activity.user_goal, agent_action=activity.action_type)
        )
        db_activity.risk_score = float(alignment_result.risk_score)
        db_activity.alignment_score = float(alignment_result.alignment_score)
        logger.info(
            f"Alignment for action={activity.action_type}: "
            f"risk={alignment_result.risk_score} alignment={alignment_result.alignment_score}"
        )

    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    logger.info(f"Created activity id={db_activity.id} action={db_activity.action_type}")

    # Step 2: Policy evaluation
    evaluation = policy_service.evaluate_action(db, activity.action_type)
    db_activity.policy_decision = evaluation.decision
    db.commit()

    # Step 3: Generate policy violation alert (warn or block)
    alert_service.generate_alert_for_policy_decision(
        db=db,
        action_type=activity.action_type,
        decision=evaluation.decision,
        matched_policy=evaluation.matched_policy,
        activity_id=db_activity.id,
    )

    # Step 4: High-risk alert
    if db_activity.risk_score is not None and db_activity.risk_score >= HIGH_RISK_THRESHOLD:
        alert_service.generate_alert_for_high_risk(
            db=db,
            action_type=activity.action_type,
            risk_score=db_activity.risk_score / 100.0,
            activity_id=db_activity.id,
        )

    # Step 5: Goal alignment failure alert
    if db_activity.alignment_score is not None and db_activity.alignment_score <= LOW_ALIGNMENT_THRESHOLD:
        alert_service.generate_alert_for_goal_alignment_failure(
            db=db,
            action_type=activity.action_type,
            activity_id=db_activity.id,
        )

    db.refresh(db_activity)
    return db_activity


def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).order_by(Activity.timestamp.desc()).offset(skip).limit(limit).all()


def get_activity(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


def update_activity(db: Session, activity_id: int, updates: dict):
    activity = get_activity(db, activity_id)
    for field, value in updates.items():
        if hasattr(activity, field):
            setattr(activity, field, value)
    db.commit()
    db.refresh(activity)
    return activity


def delete_activity(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


def get_stats(db: Session) -> dict:
    total = db.query(Activity).count()
    success = db.query(Activity).filter(Activity.status == "success").count()
    warning = db.query(Activity).filter(Activity.status == "warning").count()
    blocked = db.query(Activity).filter(Activity.status == "blocked").count()
    failed = db.query(Activity).filter(Activity.status == "failed").count()
    return {
        "total": total,
        "success": success,
        "warning": warning,
        "blocked": blocked,
        "failed": failed,
    }


def get_agent_stats(db: Session) -> list[dict]:
    """Return per-agent activity counts for multi-agent monitoring."""
    from sqlalchemy import func
    rows = (
        db.query(Activity.agent_name, func.count(Activity.id).label("total"))
        .group_by(Activity.agent_name)
        .all()
    )
    return [{"agent_name": r.agent_name, "total": r.total} for r in rows]
