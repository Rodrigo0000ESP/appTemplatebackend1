"""
FastAPI Main Application
Uses R Firm PyPI packages from requirements.txt
All packages are installed in: venv/lib/python3.x/site-packages/rodrigo0000_fastapi_core_*
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import from installed PyPI packages
from fastapi_core_database import init_db, get_db
from fastapi_core_config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="R Firm SaaS Backend using FastAPI Core Ecosystem"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "packages": {
            "auth": "rodrigo0000-fastapi-core-auth",
            "config": "rodrigo0000-fastapi-core-config",
            "controllers": "rodrigo0000-fastapi-core-controllers",
            "database": "rodrigo0000-fastapi-core-database",
            "middleware": "rodrigo0000-fastapi-core-middleware",
            "models": "rodrigo0000-fastapi-core-models",
            "services": "rodrigo0000-fastapi-core-services",
            "utils": "rodrigo0000-fastapi-core-utils",
        }
    }


@app.get("/api/v1/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to R Firm SaaS Backend",
        "docs": "/docs",
        "health": "/health"
    }


# Import routers from installed packages and local controllers
from fastapi_core_auth import router as auth_router
from app.controllers.user_controller_simple import router as user_router
from app.controllers.stripe_controller_simple import router as stripe_router
from app.controllers.email_controller_simple import router as email_router
from app.controllers.plan_controller_simple import router as plan_router

# Authentication endpoints - using router from fastapi_core_auth package
app.include_router(
    auth_router,
    prefix="/api/v1",
    tags=["Authentication"]
)

# User management endpoints
app.include_router(
    user_router,
    prefix="/api/v1/users",
    tags=["Users"]
)

# Stripe/Payment endpoints
app.include_router(
    stripe_router,
    prefix="/api/v1/stripe",
    tags=["Stripe & Payments"]
)

# Email endpoints
app.include_router(
    email_router,
    prefix="/api/v1/email",
    tags=["Email"]
)

# Plan management endpoints
app.include_router(
    plan_router,
    prefix="/api/v1/plans",
    tags=["Plans"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
