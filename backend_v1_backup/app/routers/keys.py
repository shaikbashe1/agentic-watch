from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
import hashlib
import secrets
from typing import List

from ..database import get_db
from ..models import tenant
from ..services.auth_service import get_current_user, require_admin

router = APIRouter()

class APIKeyCreateRequest(BaseModel):
    name: str

def generate_api_key(prefix="aw_live_"):
    # Generate 32 bytes of randomness and convert to hex
    raw_key = secrets.token_hex(32)
    return f"{prefix}{raw_key}"

@router.post("/api-keys", tags=["keys"])
async def create_api_key(payload: APIKeyCreateRequest, current_user: tenant.User = Depends(require_admin), db: Session = Depends(get_db)):
    workspace_id = current_user.workspace_id
    
    plaintext_key = generate_api_key()
    key_hash = hashlib.sha256(plaintext_key.encode()).hexdigest()
    key_prefix = plaintext_key[:12] # e.g. aw_live_a1b2
    
    db_key = tenant.APIKey(
        workspace_id=workspace_id,
        name=payload.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        scopes="*" # default all scopes
    )
    db.add(db_key)
    db.commit()
    
    # We return the plaintext key ONCE
    return {"id": db_key.id, "key": plaintext_key, "name": db_key.name}

@router.get("/api-keys", tags=["keys"])
async def get_api_keys(current_user: tenant.User = Depends(get_current_user), db: Session = Depends(get_db)):
    keys = db.query(tenant.APIKey).filter(tenant.APIKey.workspace_id == current_user.workspace_id).all()
    return [{"id": k.id, "name": k.name, "prefix": k.key_prefix, "revoked": k.revoked, "created_at": k.created_at} for k in keys]

@router.delete("/api-keys/{key_id}", tags=["keys"])
async def revoke_api_key(key_id: str, current_user: tenant.User = Depends(require_admin), db: Session = Depends(get_db)):
    key = db.query(tenant.APIKey).filter(tenant.APIKey.id == key_id, tenant.APIKey.workspace_id == current_user.workspace_id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
        
    key.revoked = True
    db.commit()
    return {"status": "success"}
