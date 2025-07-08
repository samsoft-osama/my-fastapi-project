"""
Main FastAPI application for Food Order Booking System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import create_tables
from app.api.v1.api import api_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A modern food ordering and management system with authentication",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint for Food Order Booking System"""
    return {
        "message": "Welcome to Food Booking Order Management System",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "api": f"{settings.API_V1_STR}",
        "endpoints": {
            "authentication": [
                f"{settings.API_V1_STR}/auth/register",
                f"{settings.API_V1_STR}/auth/token",
                f"{settings.API_V1_STR}/auth/login"
            ],
            "users": [
                f"{settings.API_V1_STR}/users/me"
            ],
            "menu": [
                f"{settings.API_V1_STR}/menu",
                f"{settings.API_V1_STR}/menu/categories"
            ],
            "orders": [
                f"{settings.API_V1_STR}/orders",
                f"{settings.API_V1_STR}/orders/history"
            ]
        }
    }

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    create_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 