from pydantic import BaseModel, Field

class VerificationRequest(BaseModel):
    claim: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Claim to be verified"
    )