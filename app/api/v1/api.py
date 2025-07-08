"""
Main API router for food order booking system
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, menu, orders

api_router = APIRouter()

# Include authentication endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include user management endpoints
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Include menu management endpoints
api_router.include_router(menu.router, prefix="/menu", tags=["menu"])

# Include order management endpoints
api_router.include_router(orders.router, prefix="/orders", tags=["orders"]) 