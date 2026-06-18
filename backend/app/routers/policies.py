from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse, PolicyEvaluationRequest, PolicyEvaluationResponse
from ..services import policy_service

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("", response_model=PolicyResponse, status_code=201)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db)):
    return policy_service.create_policy(db, policy)


@router.get("", response_model=List[PolicyResponse])
def get_policies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return policy_service.get_policies(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=PolicyResponse)
def get_policy(id: int, db: Session = Depends(get_db)):
    return policy_service.get_policy(db, id)


@router.put("/{id}", response_model=PolicyResponse)
def update_policy(id: int, policy: PolicyUpdate, db: Session = Depends(get_db)):
    return policy_service.update_policy(db, id, policy)


@router.delete("/{id}")
def delete_policy(id: int, db: Session = Depends(get_db)):
    return policy_service.delete_policy(db, id)


@router.post("/evaluate", response_model=PolicyEvaluationResponse)
def evaluate_policy(request: PolicyEvaluationRequest, db: Session = Depends(get_db)):
    return policy_service.evaluate_action(db, request.action_type)
