from fastapi import APIRouter
from typing import List, Dict

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("", response_model=List[Dict])
def get_alerts():
    return [
        {"id": 1, "severity": "Critical", "message": "Production DB deleted", "timestamp": "2026-06-18T10:00:00Z"},
        {"id": 2, "severity": "High", "message": "Policy violation: root access", "timestamp": "2026-06-18T10:05:00Z"}
    ]
