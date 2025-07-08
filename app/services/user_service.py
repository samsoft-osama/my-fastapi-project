"""
User service for user management business logic
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import security
from fastapi import HTTPException, status


class UserService:
    """Service class for user management operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if username already exists
        if UserService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if UserService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = security.get_password_hash(user_data.password)
        
        # Create user
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        
        # Update fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user"""
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def is_active_user(user: User) -> bool:
        """Check if user is active"""
        return user.is_active
    
    @staticmethod
    def is_superuser(user: User) -> bool:
        """Check if user is superuser"""
        return user.is_superuser 