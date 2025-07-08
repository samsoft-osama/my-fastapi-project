"""
Order model for order management
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Order(Base):
    """Order model for order management"""
    
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, confirmed, preparing, delivered, cancelled
    delivery_address = Column(Text, nullable=False)
    phone_number = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, status='{self.status}', total={self.total_amount})>"
    
    @property
    def formatted_total(self) -> str:
        """Get formatted total amount"""
        return f"${self.total_amount:.2f}"
    
    @property
    def is_completed(self) -> bool:
        """Check if order is completed"""
        return self.status in ["delivered", "cancelled"] 