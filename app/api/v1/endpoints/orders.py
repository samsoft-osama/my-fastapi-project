"""
Order endpoints for food order booking system
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_active_user, get_current_superuser
from app.db.base import get_db
from app.models.user import User
from app.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    status_filter: Optional[str] = Query(None, description="Filter by order status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get orders for the current user or all orders (admin)
    """
    if current_user.is_superuser:
        # Admin can see all orders
        return OrderService.get_orders(
            db, skip=skip, limit=limit, status=status_filter
        )
    else:
        # Regular users can only see their own orders
        return OrderService.get_orders(
            db, user_id=current_user.id, skip=skip, limit=limit, status=status_filter
        )


@router.get("/history", response_model=List[OrderResponse])
async def get_order_history(
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of orders to return"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get order history for the current user
    """
    return OrderService.get_user_order_history(
        db, current_user.id, skip=skip, limit=limit
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific order by ID
    """
    if current_user.is_superuser:
        # Admin can see any order
        order = OrderService.get_order(db, order_id)
    else:
        # Regular users can only see their own orders
        order = OrderService.get_order(db, order_id, current_user.id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new order
    """
    return OrderService.create_order(db, order_data, current_user.id)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an order
    """
    if current_user.is_superuser:
        # Admin can update any order
        updated_order = OrderService.update_order(db, order_id, order_data)
    else:
        # Regular users can only update their own orders
        updated_order = OrderService.update_order(db, order_id, order_data, current_user.id)
    
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return updated_order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an order
    """
    if current_user.is_superuser:
        # Admin can delete any order
        success = OrderService.delete_order(db, order_id)
    else:
        # Regular users can only delete their own orders
        success = OrderService.delete_order(db, order_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return None


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status: str = Query(..., description="New order status"),
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Update order status (Admin only)
    """
    updated_order = OrderService.update_order_status(db, order_id, status)
    if not updated_order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return updated_order


@router.get("/status/{status}", response_model=List[OrderResponse])
async def get_orders_by_status(
    status: str,
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of orders to return"),
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Get all orders with a specific status (Admin only)
    """
    return OrderService.get_orders_by_status(db, status) 