from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import logging

app = FastAPI(title="AgentWatch API V2", version="2.0.0")
security = HTTPBearer()
logger = logging.getLogger(__name__)

# Mock DB
TENANTS = {
    "tenant-1": {"id": "tenant-1", "name": "Acme Corp", "tier": "enterprise"},
    "tenant-2": {"id": "tenant-2", "name": "Stark Industries", "tier": "pro"}
}

USERS = {
    "user-1": {"id": "user-1", "tenant_id": "tenant-1", "role": "admin"},
    "user-2": {"id": "user-2", "tenant_id": "tenant-1", "role": "viewer"},
}

class User(BaseModel):
    id: str
    tenant_id: str
    role: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)) -> User:
    token = credentials.credentials
    # Mock token validation
    user_data = USERS.get(token)
    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    return User(**user_data)

def require_role(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if required_role == "admin" and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user
    return role_checker

@app.get("/api/v1/workspaces")
async def get_workspaces(user: User = Depends(require_role("viewer"))):
    """Returns workspaces scoped to the user's tenant."""
    return {"tenant": TENANTS[user.tenant_id], "status": "active"}

@app.post("/api/v1/workspaces/settings")
async def update_settings(user: User = Depends(require_role("admin"))):
    """Only admins can update workspace settings."""
    return {"message": "Settings updated successfully for tenant " + user.tenant_id}

@app.get("/health")
async def health():
    return {"status": "ok"}
