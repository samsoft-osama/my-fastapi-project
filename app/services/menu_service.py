"""
Menu service for food order booking system
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.menu_item import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate


class MenuService:
    """Service class for menu item operations"""
    
    @staticmethod
    def create_menu_item(db: Session, menu_data: MenuItemCreate) -> MenuItem:
        """Create a new menu item"""
        db_menu_item = MenuItem(
            name=menu_data.name,
            description=menu_data.description,
            price=menu_data.price,
            category=menu_data.category,
            is_available=menu_data.is_available,
            image_url=menu_data.image_url
        )
        db.add(db_menu_item)
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item
    
    @staticmethod
    def get_menu_items(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        category: Optional[str] = None,
        available_only: bool = False
    ) -> List[MenuItem]:
        """Get all menu items with optional filtering"""
        query = db.query(MenuItem)
        
        if category:
            query = query.filter(MenuItem.category == category)
        
        if available_only:
            query = query.filter(MenuItem.is_available == True)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_menu_item(db: Session, item_id: int) -> Optional[MenuItem]:
        """Get a specific menu item by ID"""
        return db.query(MenuItem).filter(MenuItem.id == item_id).first()
    
    @staticmethod
    def update_menu_item(
        db: Session, 
        item_id: int, 
        menu_data: MenuItemUpdate
    ) -> Optional[MenuItem]:
        """Update a menu item"""
        db_menu_item = MenuService.get_menu_item(db, item_id)
        if not db_menu_item:
            return None
        
        update_data = menu_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu_item, field, value)
        
        db.commit()
        db.refresh(db_menu_item)
        return db_menu_item
    
    @staticmethod
    def delete_menu_item(db: Session, item_id: int) -> bool:
        """Delete a menu item"""
        db_menu_item = MenuService.get_menu_item(db, item_id)
        if not db_menu_item:
            return False
        
        db.delete(db_menu_item)
        db.commit()
        return True
    
    @staticmethod
    def get_categories(db: Session) -> List[str]:
        """Get all available menu categories"""
        categories = db.query(MenuItem.category).distinct().all()
        return [category[0] for category in categories]
    
    @staticmethod
    def search_menu_items(
        db: Session, 
        search_term: str, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[MenuItem]:
        """Search menu items by name or description"""
        return db.query(MenuItem).filter(
            (MenuItem.name.ilike(f"%{search_term}%")) |
            (MenuItem.description.ilike(f"%{search_term}%"))
        ).offset(skip).limit(limit).all() 