from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from typing import Dict, Any

from ..database import get_db
from ..models import tenant
from ..services.auth_service import verify_password, get_password_hash, create_access_token

router = APIRouter()

class RegisterRequest(BaseModel):
    company_name: str
    email: str
    password: str

@router.post("/auth/register", tags=["auth"])
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if user already exists
    user = db.query(tenant.User).filter(tenant.User.email == request.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    company_id = f"comp_{uuid.uuid4().hex[:8]}"
    db_company = tenant.Company(id=company_id, name=request.company_name)
    db.add(db_company)
    
    user_id = f"user_{uuid.uuid4().hex[:8]}"
    hashed_pw = get_password_hash(request.password)
    db_user = tenant.User(
        id=user_id,
        company_id=company_id,
        email=request.email,
        hashed_password=hashed_pw,
        role="Owner"
    )
    db.add(db_user)
    
    db.commit()
    
    access_token = create_access_token(data={"sub": user_id, "company_id": company_id})
    return {"access_token": access_token, "token_type": "bearer"}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/login", tags=["auth"])
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(tenant.User).filter(tenant.User.email == request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token = create_access_token(data={"sub": user.id, "company_id": user.company_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/token", tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(tenant.User).filter(tenant.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.id, "company_id": user.company_id})
    return {"access_token": access_token, "token_type": "bearer"}
