"""
Updated authentication tests for the new modular structure
"""
import pytest
from fastapi import status


def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data  # Password should not be returned


def test_register_duplicate_user(client):
    """Test registration with duplicate username"""
    user_data = {
        "username": "duplicateuser",
        "email": "duplicate@example.com",
        "password": "pass123"
    }
    
    # Register first time
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    # Try to register again with same username
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_user(client):
    """Test user login"""
    # Register a user first
    user_data = {
        "username": "loginuser",
        "email": "login@example.com",
        "password": "loginpass123"
    }
    
    client.post("/api/v1/auth/register", json=user_data)
    
    # Login with JSON data
    login_data = {
        "username": user_data["username"],
        "password": user_data["password"]
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpass"
    }
    
    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers):
    """Test getting current user profile"""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_profile(client, auth_headers):
    """Test updating user profile"""
    update_data = {
        "email": "updated@example.com",
        "full_name": "Updated User"
    }
    
    response = client.put("/api/v1/auth/profile", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["email"] == update_data["email"]
    assert data["full_name"] == update_data["full_name"]


def test_change_password(client, auth_headers):
    """Test changing user password"""
    password_data = {
        "current_password": "testpass123",
        "new_password": "newpassword123"
    }
    
    response = client.put("/api/v1/auth/change-password", json=password_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    # Try to login with new password
    login_data = {
        "username": "testuser",
        "password": "newpassword123"
    }
    
    login_response = client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == status.HTTP_200_OK 