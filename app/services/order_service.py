"""
Order service for food order booking system
"""
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.menu_item import MenuItem
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate
from decimal import Decimal


class OrderService:
    """Service class for order operations"""
    
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate, user_id: int) -> Order:
        """Create a new order with order items"""
        # Calculate total amount
        total_amount = Decimal('0.0')
        
        # Create order with default status
        db_order = Order(
            user_id=user_id,
            total_amount=total_amount,
            status='pending',  # Default status for new orders
            delivery_address=order_data.delivery_address,
            phone_number=order_data.phone_number,
            notes=order_data.notes
        )
        db.add(db_order)
        db.flush()  # Get the order ID without committing
        
        # Create order items and calculate total
        for item_data in order_data.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item_data.menu_item_id).first()
            if menu_item and menu_item.is_available:
                order_item = OrderItem(
                    order_id=db_order.id,
                    menu_item_id=item_data.menu_item_id,
                    quantity=item_data.quantity,
                    price=menu_item.price
                )
                db.add(order_item)
                # Convert both price and quantity to Decimal for precise calculation
                total_amount += Decimal(str(menu_item.price)) * Decimal(str(item_data.quantity))
        
        # Update order total
        db_order.total_amount = total_amount
        db.commit()
        db.refresh(db_order)
        
        # Load the order with relationships for response
        return OrderService.get_order_with_items(db, db_order.id)
    
    @staticmethod
    def get_orders(
        db: Session, 
        user_id: Optional[int] = None,
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Order]:
        """Get orders with optional filtering"""
        query = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.menu_item)
        )
        
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        if status:
            query = query.filter(Order.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_order(db: Session, order_id: int, user_id: Optional[int] = None) -> Optional[Order]:
        """Get a specific order by ID"""
        return OrderService.get_order_with_items(db, order_id, user_id)
    
    @staticmethod
    def get_order_with_items(db: Session, order_id: int, user_id: Optional[int] = None) -> Optional[Order]:
        """Get a specific order by ID with loaded relationships"""
        query = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.menu_item)
        ).filter(Order.id == order_id)
        
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        return query.first()
    
    @staticmethod
    def update_order(
        db: Session, 
        order_id: int, 
        order_data: OrderUpdate,
        user_id: Optional[int] = None
    ) -> Optional[Order]:
        """Update an order"""
        query = db.query(Order).filter(Order.id == order_id)
        
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        db_order = query.first()
        if not db_order:
            return None
        
        update_data = order_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        
        # Return order with loaded relationships
        return OrderService.get_order_with_items(db, order_id, user_id)
    
    @staticmethod
    def delete_order(db: Session, order_id: int, user_id: Optional[int] = None) -> bool:
        """Delete an order"""
        query = db.query(Order).filter(Order.id == order_id)
        
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        db_order = query.first()
        if not db_order:
            return False
        
        # Delete associated order items first
        db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
        
        # Delete the order
        db.delete(db_order)
        db.commit()
        return True
    
    @staticmethod
    def get_order_items(db: Session, order_id: int) -> List[OrderItem]:
        """Get all items for a specific order"""
        return db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
    
    @staticmethod
    def update_order_status(db: Session, order_id: int, status: str) -> Optional[Order]:
        """Update order status"""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None
        
        db_order.status = status
        db.commit()
        db.refresh(db_order)
        
        # Return order with loaded relationships
        return OrderService.get_order_with_items(db, order_id)
    
    @staticmethod
    def get_user_order_history(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 50
    ) -> List[Order]:
        """Get order history for a specific user"""
        return db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.menu_item)
        ).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_orders_by_status(db: Session, status: str) -> List[Order]:
        """Get all orders with a specific status"""
        return db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.menu_item)
        ).filter(Order.status == status).all()
    
    @staticmethod
    def calculate_order_total(db: Session, order_id: int) -> Decimal:
        """Calculate total amount for an order"""
        order_items = OrderService.get_order_items(db, order_id)
        total = Decimal('0.0')
        for item in order_items:
            total += Decimal(str(item.price)) * Decimal(str(item.quantity))
        return total 