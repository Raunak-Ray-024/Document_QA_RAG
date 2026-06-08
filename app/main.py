import sys
import os

print("=== STARTING APP ===")
print(f"PORT env var: {os.environ.get('PORT', 'NOT SET')}")

# Step 1: Test config
try:
    from app.config import settings
    print(f"✅ Config loaded. DATABASE_URL starts with: {settings.DATABASE_URL[:50] if settings.DATABASE_URL else 'NOT SET'}...")
except Exception as e:
    print(f"❌ Config error: {e}")
    sys.exit(1)

# Step 2: Test database module
try:
    from app.database import init_db, get_db
    print("✅ Database module imported")
except Exception as e:
    print(f"❌ Database import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 3: Test routers
try:
    from app.routers import documents, query
    print("✅ Routers imported")
except Exception as e:
    print(f"❌ Routers import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Import FastAPI and other modules
try:
    from fastapi import FastAPI, Depends, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from sqlalchemy.orm import Session
    from app.schemas import HealthResponse
    print("✅ FastAPI and dependencies imported")
except Exception as e:
    print(f"❌ FastAPI import error: {e}")
    sys.exit(1)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="RAG-based Document Q&A System with FastAPI + pgvector",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Run when FastAPI starts"""
    print("🚀 Starting RAG System API...")
    print("🔧 Initializing database...")
    try:
        init_db()
        print("✅ Database initialized with pgvector support")
    except Exception as e:
        print(f"❌ Database init error: {e}")
        raise
    print(f"📚 Using embedding model: {settings.embedding_model}")

# Include routers
app.include_router(documents.router)
app.include_router(query.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Document Q&A RAG System",
        "version": settings.app_version,
        "docs": "/docs",
        "endpoints": {
            "upload": "POST /documents/upload",
            "list_documents": "GET /documents/",
            "get_document": "GET /documents/{document_id}",
            "delete_document": "DELETE /documents/{document_id}",
            "ask": "POST /query/ask"
        }
    }

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Check if the API and database are working"""
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        version=settings.app_version
    )

print("✅ App creation complete")