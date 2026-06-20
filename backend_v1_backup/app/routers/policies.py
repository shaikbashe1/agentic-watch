from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse, PolicyEvaluationRequest, PolicyEvaluationResponse
from ..services import policy_service
from ..services.auth_service import get_current_user, get_workspace_from_api_key, require_admin
from ..models import tenant

router = APIRouter(prefix="/policies", tags=["policies"])


@router.post("", response_model=PolicyResponse, status_code=201)
def create_policy(policy: PolicyCreate, current_user: tenant.User = Depends(require_admin), db: Session = Depends(get_db)):
    return policy_service.create_policy(db, current_user.workspace_id, policy)


@router.get("", response_model=List[PolicyResponse])
def get_policies(skip: int = 0, limit: int = 100, current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return policy_service.get_policies(db, current_user.workspace_id, skip=skip, limit=limit)


@router.get("/{id}", response_model=PolicyResponse)
def get_policy(id: str, current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return policy_service.get_policy(db, current_user.workspace_id, id)


@router.put("/{id}", response_model=PolicyResponse)
def update_policy(id: str, policy: PolicyUpdate, current_user: tenant.User = Depends(require_admin), db: Session = Depends(get_db)):
    return policy_service.update_policy(db, current_user.workspace_id, id, policy)


@router.delete("/{id}")
def delete_policy(id: str, current_user: tenant.User = Depends(require_admin), db: Session = Depends(get_db)):
    return policy_service.delete_policy(db, current_user.workspace_id, id)


@router.post("/evaluate", response_model=PolicyEvaluationResponse)
def evaluate_policy(request: PolicyEvaluationRequest, workspace_id: str = Depends(get_workspace_from_api_key), db: Session = Depends(get_db)):
    # Lazy import to avoid circular dependency before we write it
    from ..services.policy_engine import PolicyEngine
    engine = PolicyEngine(db)
    return engine.evaluate(workspace_id, request.payload)
