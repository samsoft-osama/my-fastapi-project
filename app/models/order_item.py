"""
Order item model for order line items
"""
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class OrderItem(Base):
    """Order item model for order line items"""
    
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)  # Price at time of order
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    menu_item = relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem(id={self.id}, order_id={self.order_id}, menu_item_id={self.menu_item_id}, quantity={self.quantity})>"
    
    @property
    def total_price(self) -> float:
        """Calculate total price for this item"""
        return self.price * self.quantity
    
    @property
    def formatted_total(self) -> str:
        """Get formatted total price"""
        return f"${self.total_price:.2f}" 