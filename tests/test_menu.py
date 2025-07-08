import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_menu.db"
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

def get_auth_token():
    # Register and login to get token
    client.post(
        "/register",
        json={"username": "menuuser", "email": "menu@example.com", "password": "menupass123"}
    )
    
    login_response = client.post(
        "/token",
        data={"username": "menuuser", "password": "menupass123"}
    )
    return login_response.json()["access_token"]

def test_create_menu_item():
    token = get_auth_token()
    
    response = client.post(
        "/menu",
        json={
            "name": "Pizza Margherita",
            "description": "Classic pizza with tomato and mozzarella",
            "price": 12.99,
            "category": "Pizza"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pizza Margherita"
    assert data["price"] == 12.99

def test_get_menu_items():
    token = get_auth_token()
    
    # Create a menu item first
    client.post(
        "/menu",
        json={
            "name": "Burger",
            "description": "Beef burger with fries",
            "price": 8.99,
            "category": "Main Course"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = client.get("/menu")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_menu_item():
    token = get_auth_token()
    
    # Create a menu item
    create_response = client.post(
        "/menu",
        json={
            "name": "Pasta",
            "description": "Creamy pasta with chicken",
            "price": 10.99,
            "category": "Main Course"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]
    
    response = client.get(f"/menu/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pasta"

def test_update_menu_item():
    token = get_auth_token()
    
    # Create a menu item
    create_response = client.post(
        "/menu",
        json={
            "name": "Salad",
            "description": "Fresh green salad",
            "price": 6.99,
            "category": "Appetizer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]
    
    # Update the item
    response = client.put(
        f"/menu/{item_id}",
        json={"price": 7.99},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 7.99

def test_delete_menu_item():
    token = get_auth_token()
    
    # Create a menu item
    create_response = client.post(
        "/menu",
        json={
            "name": "Soup",
            "description": "Hot tomato soup",
            "price": 4.99,
            "category": "Appetizer"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(
        f"/menu/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/menu/{item_id}")
    assert get_response.status_code == 404 