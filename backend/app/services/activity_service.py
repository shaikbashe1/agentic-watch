import logging
from sqlalchemy.orm import Session
from ..models.activity import Activity
from ..schemas.activity import ActivityCreate
from fastapi import HTTPException
from . import policy_service, alert_service

logger = logging.getLogger(__name__)


def create_activity(db: Session, activity: ActivityCreate) -> Activity:
    db_activity = Activity(
        agent_name=activity.agent_name,
        action_type=activity.action_type,
        action_description=activity.action_description,
        target_resource=activity.target_resource,
        status=activity.status,
        metadata_=activity.metadata_,
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    logger.info(f"Created activity id={db_activity.id} action={db_activity.action_type}")

    # Policy evaluation
    evaluation = policy_service.evaluate_action(db, activity.action_type)
    alert_service.generate_alert_for_policy_decision(
        db=db,
        action_type=activity.action_type,
        decision=evaluation.decision,
        matched_policy=evaluation.matched_policy,
        activity_id=db_activity.id,
    )

    return db_activity


def get_activities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Activity).offset(skip).limit(limit).all()


def get_activity(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity


def delete_activity(db: Session, activity_id: int):
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}


def get_stats(db: Session):
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
