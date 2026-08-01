from fastapi import APIRouter
from app.schemas.request import VerificationRequest
from app.services.verification_service import verify_claim

router = APIRouter()

@router.post("/verify")
def verify(request: VerificationRequest):
    return verify_claim(request.claim)