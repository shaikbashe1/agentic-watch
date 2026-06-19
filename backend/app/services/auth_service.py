from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import tenant

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(tenant.User).filter(tenant.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

import hashlib

async def get_workspace_from_api_key(api_key: str = Depends(api_key_header), db: Session = Depends(get_db)):
    if not api_key:
        raise HTTPException(status_code=401, detail="X-API-Key header missing")
    
    # Hash the incoming key to compare with the database
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    key_record = db.query(tenant.APIKey).filter(tenant.APIKey.key_hash == key_hash).first()
    
    if not key_record or key_record.revoked:
        raise HTTPException(status_code=401, detail="Invalid or Revoked API Key")
    return key_record.workspace_id
