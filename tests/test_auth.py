import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login_user():
    # First register a user
    client.post(
        "/register",
        json={"username": "loginuser", "email": "login@example.com", "password": "loginpass123"}
    )
    
    # Then login
    response = client.post(
        "/token",
        data={"username": "loginuser", "password": "loginpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    response = client.post(
        "/token",
        data={"username": "nonexistent", "password": "wrongpass"}
    )
    assert response.status_code == 401

def test_get_current_user():
    # Register and login
    client.post(
        "/register",
        json={"username": "currentuser", "email": "current@example.com", "password": "currentpass123"}
    )
    
    login_response = client.post(
        "/token",
        data={"username": "currentuser", "password": "currentpass123"}
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "currentuser" 