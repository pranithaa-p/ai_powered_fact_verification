from pydantic import BaseModel

class VerificationResponse(BaseModel):
    verdict: str
    confidence: float
    explanation: str