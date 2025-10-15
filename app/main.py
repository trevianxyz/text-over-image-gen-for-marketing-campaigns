# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import routes
from app.services.logging_db import init_db, close_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events"""
    # Startup
    print("🚀 Starting up Creative Automation Pipeline...")
    init_db()
    yield
    # Shutdown
    print("🛑 Shutting down Creative Automation Pipeline...")
    close_db()

# Initialize FastAPI with lifespan
app = FastAPI(
    title="Creative Automation Pipeline",
    description="Automated campaign creative generator",
    version="0.1.0",
    lifespan=lifespan,
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