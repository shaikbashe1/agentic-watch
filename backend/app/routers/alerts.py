from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.alert import AlertCreate, AlertUpdate, AlertResponse
from ..services import alert_service

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.post("", response_model=AlertResponse, status_code=201)
def create_alert(alert: AlertCreate, db: Session = Depends(get_db)):
    return alert_service.create_alert(db, alert)


@router.get("", response_model=List[AlertResponse])
def get_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return alert_service.get_alerts(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=AlertResponse)
def get_alert(id: int, db: Session = Depends(get_db)):
    return alert_service.get_alert(db, id)


@router.put("/{id}", response_model=AlertResponse)
def update_alert(id: int, alert: AlertUpdate, db: Session = Depends(get_db)):
    return alert_service.update_alert(db, id, alert)


@router.delete("/{id}")
def delete_alert(id: int, db: Session = Depends(get_db)):
    return alert_service.delete_alert(db, id)
