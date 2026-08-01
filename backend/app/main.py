from fastapi import FastAPI
from app.api.routes import router
from fastapi.responses import JSONResponse
from fastapi import Request


app = FastAPI(
    title="Decipher API",
    description="AI-Powered Fact Verification Agent",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Decipher API",
        "status": "Running"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc)
        }
    )