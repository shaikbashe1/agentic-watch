import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ..models.alert import Alert
from ..schemas.alert import AlertCreate, AlertUpdate
from . import notification_service

logger = logging.getLogger(__name__)

_DECISION_SEVERITY = {
    "block": "critical",
    "warn": "medium",
    "allow": "low",
}


def create_alert(db: Session, alert: AlertCreate) -> Alert:
    db_alert = Alert(
        title=alert.title,
        description=alert.description,
        severity=alert.severity.value,
        source=alert.source,
        activity_id=alert.activity_id,
        status=alert.status.value,
    )
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    logger.info(f"Created alert id={db_alert.id} severity={db_alert.severity}")
    notification_service.notify_alert(
        alert_title=db_alert.title,
        alert_description=db_alert.description,
        severity=db_alert.severity,
        activity_id=db_alert.activity_id,
    )
    return db_alert


def get_alerts(db: Session, skip: int = 0, limit: int = 100) -> list[Alert]:
    return db.query(Alert).offset(skip).limit(limit).all()


def get_alert(db: Session, alert_id: int) -> Alert:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


def update_alert(db: Session, alert_id: int, alert_update: AlertUpdate) -> Alert:
    alert = get_alert(db, alert_id)
    update_data = alert_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(value, "value"):
            value = value.value
        setattr(alert, field, value)
    db.commit()
    db.refresh(alert)
    logger.info(f"Updated alert id={alert_id}")
    return alert


def delete_alert(db: Session, alert_id: int) -> dict:
    alert = get_alert(db, alert_id)
    db.delete(alert)
    db.commit()
    logger.info(f"Deleted alert id={alert_id}")
    return {"message": "Alert deleted successfully"}


def generate_alert_for_policy_decision(
    db: Session,
    action_type: str,
    decision: str,
    matched_policy: Optional[str],
    activity_id: Optional[int],
) -> Optional[Alert]:
    """Generate an alert when policy evaluation yields warn or block."""
    if decision == "allow":
        return None

    severity = _DECISION_SEVERITY.get(decision, "medium")
    title = f"Policy {decision.upper()}: {action_type}"
    description = (
        f"Action '{action_type}' was {decision}ed"
        + (f" by policy '{matched_policy}'" if matched_policy else "")
        + "."
    )
    alert_data = AlertCreate(
        title=title,
        description=description,
        severity=severity,
        source="policy_engine",
        activity_id=activity_id,
        status="open",
    )
    return create_alert(db, alert_data)


def generate_alert_for_high_risk(
    db: Session,
    action_type: str,
    risk_score: float,
    activity_id: Optional[int],
) -> Alert:
    severity = "critical" if risk_score >= 0.9 else "high"
    alert_data = AlertCreate(
        title=f"High Risk Score: {action_type}",
        description=f"Action '{action_type}' has risk score {risk_score:.2f}.",
        severity=severity,
        source="risk_engine",
        activity_id=activity_id,
        status="open",
    )
    return create_alert(db, alert_data)


def generate_alert_for_goal_alignment_failure(
    db: Session,
    action_type: str,
    activity_id: Optional[int],
) -> Alert:
    alert_data = AlertCreate(
        title=f"Goal Alignment Failure: {action_type}",
        description=f"Action '{action_type}' failed goal alignment check.",
        severity="high",
        source="alignment_engine",
        activity_id=activity_id,
        status="open",
    )
    return create_alert(db, alert_data)
