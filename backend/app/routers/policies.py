from fastapi import APIRouter
from typing import List, Dict

router = APIRouter(prefix="/policies", tags=["policies"])

@router.get("", response_model=List[Dict])
def get_policies():
    return [
        {"id": 1, "name": "No Destructive Actions", "enabled": True},
        {"id": 2, "name": "Require Approval for DB", "enabled": True}
    ]
