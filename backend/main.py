"""FastAPI application entry point"""
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.database import create_db_and_tables, engine
from src.models import SQLModel
from src.api.tasks import router as tasks_router
from src.auth.jwt_utils import get_jwt_secret

# Load environment variables
load_dotenv()


def validate_environment():
    """Validate required environment variables on startup"""
    try:
        # Validate BETTER_AUTH_SECRET
        secret = get_jwt_secret()
        print(f"✓ BETTER_AUTH_SECRET configured (length: {len(secret)} characters)")

        # Validate DATABASE_URL
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not configured")
        print("✓ DATABASE_URL configured")

    except ValueError as e:
        print(f"\n❌ STARTUP VALIDATION FAILED: {str(e)}\n")
        print("Required environment variables:")
        print("  - BETTER_AUTH_SECRET (minimum 32 characters)")
        print("  - DATABASE_URL (PostgreSQL connection string)")
        print("\nGenerate BETTER_AUTH_SECRET with: openssl rand -base64 48")
        print("See: specs/002-authentication-jwt/ARCHITECTURE.md for setup instructions")
        sys.exit(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup: Validate environment
    validate_environment()

    # Startup: Create database tables
    create_db_and_tables()
    print("Database tables created successfully")

    yield
    # Shutdown: Close database connections
    # SQLModel/SQLAlchemy handles this automatically


# Create FastAPI application
app = FastAPI(
    title="Todo Backend API",
    description="Backend API for multi-user todo task management",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
# SECURITY: Restrict to specific origins instead of wildcard
# In production, set to actual frontend domain(s)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,  # Restrict to specific origins
    allow_credentials=True,  # Required for HttpOnly cookie transmission
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],  # Explicit methods
    allow_headers=["Content-Type", "Authorization"],  # Explicit headers
)


# Include routers
app.include_router(tasks_router)


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Todo Backend API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
