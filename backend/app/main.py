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
import os
from pathlib import Path

# Get the project root directory (parent of backend)
project_root = Path(__file__).parent.parent.parent
frontend_static = project_root / "frontend" / "static"
frontend_templates = project_root / "frontend" / "templates"
assets_dir = project_root / "assets"

# Debug: Print paths to verify they exist
print(f"🔍 Debug paths:")
print(f"  Project root: {project_root}")
print(f"  Frontend static: {frontend_static} - exists: {frontend_static.exists()}")
print(f"  Frontend templates: {frontend_templates} - exists: {frontend_templates.exists()}")
print(f"  Assets dir: {assets_dir} - exists: {assets_dir.exists()}")

app.mount("/static", StaticFiles(directory=str(frontend_static)), name="static")
app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
templates = Jinja2Templates(directory=str(frontend_templates))

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

# Add countries endpoint directly to main app
from app.services.country_language import get_country_selector_data

@app.get("/api/countries")
def get_countries():
    """Get all available countries for the country selector"""
    try:
        data = get_country_selector_data()
        print(f"🌍 Serving {len(data.get('countries', []))} countries to frontend")
        return data
    except Exception as e:
        print(f"❌ Error serving countries data: {e}")
        return {"error": "Failed to load countries data", "countries": [], "regions": []}

# Add audience endpoint
from app.services.audience_selector import get_audience_selector_data

@app.get("/api/audiences")
def get_audiences():
    """Get all available audiences for the audience selector"""
    try:
        data = get_audience_selector_data()
        print(f"👥 Serving {data.get('total_count', 0)} audiences to frontend")
        return data
    except Exception as e:
        print(f"❌ Error serving audiences data: {e}")
        return {"error": "Failed to load audiences data", "audiences": [], "categories": {}}

@app.get("/api/master-manifest")
def get_master_manifest():
    """Get the master manifest containing all campaign data"""
    try:
        import json
        from pathlib import Path
        
        manifest_path = Path("assets/generated/master_manifest.json")
        if not manifest_path.exists():
            return {"error": "Master manifest not found. Run generate_master_manifest.py first."}
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        print(f"📋 Serving master manifest with {manifest['manifest_info']['total_campaigns']} campaigns")
        return manifest
    except Exception as e:
        print(f"❌ Error serving master manifest: {e}")
        return {"error": f"Failed to load master manifest: {e}"}