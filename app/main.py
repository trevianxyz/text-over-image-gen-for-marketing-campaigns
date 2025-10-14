# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes

# Initialize FastAPI
app = FastAPI(
    title="Creative Automation Pipeline",
    description="Automated campaign creative generator",
    version="0.1.0",
)

# Optional: allow local frontend / demo tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check
@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Creative Automation Pipeline is running",
        "endpoints": ["/campaigns/generate"]
    }

# Include campaign routes
app.include_router(routes.router, prefix="/campaigns", tags=["campaigns"])