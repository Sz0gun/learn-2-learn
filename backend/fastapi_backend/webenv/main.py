# backend/fastapi_backend/webenv/main.py
from fastapi import FastAPI
from .routers import github

app = FastAPI(
    title="WebEnv API",
    description="API for managing web environment and related functionalities.",
    version="0.1.0"
    )

# Include routers for different operations
app.include_router(github.router, prefix="/github", tags=["GitHub"])

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint for WebEnv
    """
    return {"message": "Welcome to the Learn-2-Learn Web Environment"}