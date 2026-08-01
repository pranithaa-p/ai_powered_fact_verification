from fastapi import APIRouter
from app.api.verify import router as verify_router

router = APIRouter()

router.include_router(
    verify_router,
    prefix="/api",
    tags=["Fact Verification"]
)