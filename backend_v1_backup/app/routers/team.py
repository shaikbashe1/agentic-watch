from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from ..database import get_db
from ..models import tenant
from ..services.auth_service import get_current_user, get_password_hash

router = APIRouter()

class InviteRequest(BaseModel):
    email: str
    role: str # Admin, Developer, Viewer

@router.get("/team", tags=["team"])
async def get_team(current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(tenant.User).filter(tenant.User.company_id == current_user.company_id).all()
    return [{"id": u.id, "email": u.email, "role": u.role, "created_at": u.created_at} for u in users]

@router.post("/team/invite", tags=["team"])
async def invite_member(request: InviteRequest, current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role not in ["Owner", "Admin"]:
        raise HTTPException(status_code=403, detail="Only Owners and Admins can invite new members")
        
    existing_user = db.query(tenant.User).filter(tenant.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
        
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    # Give them a dummy default password for now
    default_pw = get_password_hash("changeme123")
    
    new_user = tenant.User(
        id=user_id,
        company_id=current_user.company_id,
        email=request.email,
        hashed_password=default_pw,
        role=request.role
    )
    db.add(new_user)
    db.commit()
    
    return {"status": "success", "user_id": user_id, "email": request.email, "role": request.role}
