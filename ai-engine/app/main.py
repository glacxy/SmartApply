from fastapi import FastAPI
from app.routes import resume

app = FastAPI(
    title="SmartApply AI",
    description="AI-powered Job Application Platform",
    version="1.0.0"
)

app.include_router(
    resume.router,
    prefix="/api/resume",
    tags=["Resume"]
)

@app.get("/")
def home():
    return {
        "message": "Welcome to SmartApply AI"
    }

@app.get("/health")
def health():
    return {
        "status": "running"
    }