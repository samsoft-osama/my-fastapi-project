"""
Order schemas for request/response validation
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from app.schemas.menu import MenuItemResponse


class OrderItemBase(BaseModel):
    """Base order item schema"""
    menu_item_id: int
    quantity: int
    
    @validator('quantity')
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v


class OrderItemCreate(OrderItemBase):
    """Schema for order item creation"""
    pass


class OrderItemResponse(OrderItemBase):
    """Schema for order item response"""
    id: int
    price: float
    menu_item: MenuItemResponse  # Use proper MenuItemResponse schema
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    """Base order schema"""
    delivery_address: str
    phone_number: str
    notes: Optional[str] = None
    
    @validator('delivery_address')
    def address_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Delivery address cannot be empty')
        return v.strip()
    
    @validator('phone_number')
    def phone_number_format(cls, v):
        # Basic phone number validation
        if not v.replace('+', '').replace('-', '').replace(' ', '').replace('(', '').replace(')', '').isdigit():
            raise ValueError('Phone number must contain only digits and common separators')
        return v


class OrderCreate(OrderBase):
    """Schema for order creation"""
    items: List[OrderItemCreate]
    
    @validator('items')
    def items_not_empty(cls, v):
        if not v:
            raise ValueError('Order must contain at least one item')
        return v


class OrderUpdate(BaseModel):
    """Schema for order updates"""
    status: Optional[str] = None
    delivery_address: Optional[str] = None
    phone_number: Optional[str] = None
    notes: Optional[str] = None
    
    @validator('status')
    def valid_status(cls, v):
        if v is not None and v not in ['pending', 'confirmed', 'preparing', 'delivered', 'cancelled']:
            raise ValueError('Invalid order status')
        return v


class OrderResponse(OrderBase):
    """Schema for order response"""
    id: int
    user_id: int
    total_amount: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    order_items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True


class OrderList(BaseModel):
    """Schema for order list response"""
    orders: List[OrderResponse]
    total: int
    page: int
    size: int 