"""
Menu item schemas for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime


class MenuItemBase(BaseModel):
    """Base menu item schema"""
    name: str
    description: str
    price: float
    category: str
    image_url: Optional[str] = None
    
    @validator('price')
    def price_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class MenuItemCreate(MenuItemBase):
    """Schema for menu item creation"""
    pass


class MenuItemUpdate(BaseModel):
    """Schema for menu item updates"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None
    
    @validator('price')
    def price_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v


class MenuItemResponse(MenuItemBase):
    """Schema for menu item response"""
    id: int
    is_available: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class MenuItemList(BaseModel):
    """Schema for menu item list response"""
    items: list[MenuItemResponse]
    total: int
    page: int
    size: int 