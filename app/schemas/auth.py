"""
Authentication schemas for login and tokens
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""
    username: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema for login request"""
    username: str
    password: str


class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str 