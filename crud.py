from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
import models
import schemas
from auth import get_password_hash, verify_password

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Menu Item CRUD operations
def get_menu_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.MenuItem).offset(skip).limit(limit).all()

def get_menu_item(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def create_menu_item(db: Session, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_menu_item(db: Session, item_id: int, item: schemas.MenuItemUpdate):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_menu_item(db: Session, item_id: int):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

# Order CRUD operations
def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Order).filter(models.Order.user_id == user_id).offset(skip).limit(limit).all()

def get_order(db: Session, order_id: int, user_id: int):
    return db.query(models.Order).filter(
        and_(models.Order.id == order_id, models.Order.user_id == user_id)
    ).first()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    # Calculate total amount
    total_amount = 0
    order_items = []
    
    for item in order.items:
        menu_item = get_menu_item(db, item.menu_item_id)
        if not menu_item or not menu_item.is_available:
            raise ValueError(f"Menu item {item.menu_item_id} is not available")
        
        item_total = menu_item.price * item.quantity
        total_amount += item_total
        
        order_items.append({
            "menu_item_id": item.menu_item_id,
            "quantity": item.quantity,
            "price": item_total
        })
    
    # Create order
    db_order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        delivery_address=order.delivery_address,
        phone_number=order.phone_number
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item_data in order_items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(db_order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate, user_id: int):
    db_order = db.query(models.Order).filter(
        and_(models.Order.id == order_id, models.Order.user_id == user_id)
    ).first()
    
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int, user_id: int):
    db_order = db.query(models.Order).filter(
        and_(models.Order.id == order_id, models.Order.user_id == user_id)
    ).first()
    
    if db_order:
        # Delete order items first
        db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).delete()
        # Delete order
        db.delete(db_order)
        db.commit()
    return db_order 