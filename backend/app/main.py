# app/main.py

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Mount static files and templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

# Optional: allow local frontend / demo tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root - serve HTML frontend
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Health check API endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "message": "Creative Automation Pipeline is running",
        "endpoints": ["/campaigns/generate"]
    }

# Include campaign routes
app.include_router(routes.router, prefix="/campaigns", tags=["campaigns"])