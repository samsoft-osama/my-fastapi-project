"""
Pytest configuration and fixtures for testing
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.api.dependencies import get_db
from app.main import app

# Test database configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Clean up tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    """Create authentication headers for testing"""
    # Register a test user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    print(f"Register response: {register_response.status_code} - {register_response.text}")
    
    # Login to get token using JSON data
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"Login response: {response.status_code} - {response.text}")
    
    if response.status_code != 200:
        raise Exception(f"Login failed: {response.status_code} - {response.text}")
    
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client):
    """Create admin authentication headers for testing"""
    # Register an admin user
    user_data = {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass123",
        "is_superuser": True
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    print(f"Admin register response: {register_response.status_code} - {register_response.text}")
    
    # Login to get token using JSON data
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    print(f"Admin login response: {response.status_code} - {response.text}")
    
    if response.status_code != 200:
        raise Exception(f"Admin login failed: {response.status_code} - {response.text}")
    
    token = response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"} 