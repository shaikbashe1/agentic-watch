from fastapi import APIRouter
from ..schemas.alignment import AlignmentRequest, AlignmentResponse
from ..services import alignment_service

router = APIRouter(prefix="/alignments", tags=["alignments"])

@router.post("", response_model=AlignmentResponse)
def evaluate_alignment(request: AlignmentRequest):
    return alignment_service.evaluate_alignment(request)
