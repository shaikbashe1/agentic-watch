from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from app.core.security import create_access_token, verify_password, get_password_hash
from datetime import timedelta

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    email: str
    password: str
    workspace_name: str

# In-memory mock DB for Phase 1 skeleton (will be replaced by Postgres)
USERS_DB = {}

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    if user.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    # Mock user creation
    USERS_DB[user.email] = {
        "email": user.email,
        "hashed_password": hashed_password,
        "workspace_id": "workspace-123"
    }
    
    access_token = create_access_token(
        data={"sub": user.email, "workspace_id": "workspace-123"}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = USERS_DB.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user["email"], "workspace_id": user["workspace_id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}
