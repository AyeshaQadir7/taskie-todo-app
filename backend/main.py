"""FastAPI application entry point"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.database import create_db_and_tables, engine
from src.models import SQLModel
from src.api.tasks import router as tasks_router

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
