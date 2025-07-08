"""
Application configuration settings
"""
import os
from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    APP_NAME: str = "Food Booking Order Management System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "food_orders_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8080"]
    
    # API
    API_V1_STR: str = "/api/v1"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from components"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("DB_PASSWORD")
    def validate_db_password(cls, v):
        if not v or v == "password":
            raise ValueError("Please set a proper database password")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings() 