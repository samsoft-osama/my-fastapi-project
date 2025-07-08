"""
Menu endpoints for food order booking system
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_current_active_user, get_current_superuser
from app.db.base import get_db
from app.models.user import User
from app.schemas.menu import MenuItemResponse, MenuItemCreate, MenuItemUpdate
from app.services.menu_service import MenuService

router = APIRouter()


@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    category: Optional[str] = Query(None, description="Filter by category"),
    available_only: bool = Query(False, description="Show only available items"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: Session = Depends(get_db)
):
    """
    Get all menu items with optional filtering and search
    """
    if search:
        return MenuService.search_menu_items(db, search, skip, limit)
    else:
        return MenuService.get_menu_items(
            db, skip=skip, limit=limit, 
            category=category, available_only=available_only
        )


@router.get("/categories", response_model=List[str])
async def get_categories(db: Session = Depends(get_db)):
    """
    Get all available menu categories
    """
    return MenuService.get_categories(db)


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific menu item by ID
    """
    menu_item = MenuService.get_menu_item(db, item_id)
    if not menu_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return menu_item


@router.post("/", response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_item(
    menu_data: MenuItemCreate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Create a new menu item (Admin only)
    """
    return MenuService.create_menu_item(db, menu_data)


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    menu_data: MenuItemUpdate,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Update a menu item (Admin only)
    """
    updated_item = MenuService.update_menu_item(db, item_id, menu_data)
    if not updated_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(get_current_superuser),
    db: Session = Depends(get_db)
):
    """
    Delete a menu item (Admin only)
    """
    success = MenuService.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return None 