from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api.webhooks import router as webhook_router
from app.db.database import init_db, close_db

# Initialize FastAPI app
app = FastAPI(
    title="Lead Capture Agent",
    description="Smart lead capture system for multi-channel messaging",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook_router, prefix="/api", tags=["webhooks"])

# Serve static files (dashboard)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("[OK] Lead Capture Agent started")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    close_db()
    print("[OK] Lead Capture Agent stopped")


# Root endpoint
@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "Agent running",
        "service": "Lead Capture Agent",
        "version": "1.0.0",
        "endpoints": {
            "dashboard": "/static/dashboard.html",
            "webhook": "/api/webhook",
            "stats": "/api/webhook/stats",
            "leads": "/api/webhook/leads"
        }
    }


# Health check endpoint
@app.get("/health")
def health_check():
    """Extended health check"""
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }

