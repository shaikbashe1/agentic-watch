from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.activity import ActivityCreate, ActivityResponse
from ..services import activity_service

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=201)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    return activity_service.create_activity(db, activity)


@router.get("", response_model=List[ActivityResponse])
def get_activities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return activity_service.get_activities(db, skip=skip, limit=limit)


@router.get("/stats/agents")
def get_agent_stats(db: Session = Depends(get_db)):
    return activity_service.get_agent_stats(db)


@router.get("/{id}", response_model=ActivityResponse)
def get_activity(id: int, db: Session = Depends(get_db)):
    return activity_service.get_activity(db, id)


@router.put("/{id}", response_model=ActivityResponse)
def update_activity(id: int, updates: dict, db: Session = Depends(get_db)):
    return activity_service.update_activity(db, id, updates)


@router.delete("/{id}")
def delete_activity(id: int, db: Session = Depends(get_db)):
    return activity_service.delete_activity(db, id)
