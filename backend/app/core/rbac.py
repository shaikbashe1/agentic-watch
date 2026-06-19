from enum import Enum
from fastapi import HTTPException, Security, Depends
from typing import List

class Role(str, Enum):
    OWNER = "owner"       # full access, billing, delete workspace
    ADMIN = "admin"       # full access except billing/delete
    DEVELOPER = "developer" # read/write, no policy management
    VIEWER = "viewer"     # read-only
    BILLING = "billing"   # billing only

# Priority of roles (lower index = higher privilege)
ROLE_HIERARCHY = {
    Role.OWNER: 0,
    Role.ADMIN: 1,
    Role.DEVELOPER: 2,
    Role.VIEWER: 3,
    Role.BILLING: 4
}

def require_role(min_role: Role):
    def role_checker(current_user_role: Role = Role.VIEWER): # Mock current user role extractor
        if ROLE_HIERARCHY[current_user_role] > ROLE_HIERARCHY[min_role]:
            raise HTTPException(status_code=403, detail=f"Insufficient permissions. Requires {min_role.value} or higher.")
        return current_user_role
    return role_checker
