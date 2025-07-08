import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db
from main import app

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_orders.db"
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
        json={"username": "orderuser", "email": "order@example.com", "password": "orderpass123"}
    )
    
    login_response = client.post(
        "/token",
        data={"username": "orderuser", "password": "orderpass123"}
    )
    return login_response.json()["access_token"]

def create_menu_item():
    token = get_auth_token()
    
    response = client.post(
        "/menu",
        json={
            "name": "Test Pizza",
            "description": "Test pizza for orders",
            "price": 15.99,
            "category": "Pizza"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()["id"], token

def test_create_order():
    item_id, token = create_menu_item()
    
    response = client.post(
        "/orders",
        json={
            "delivery_address": "123 Test Street",
            "phone_number": "1234567890",
            "items": [
                {"menu_item_id": item_id, "quantity": 2}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["delivery_address"] == "123 Test Street"
    assert data["total_amount"] == 31.98

def test_get_orders():
    item_id, token = create_menu_item()
    
    # Create an order first
    client.post(
        "/orders",
        json={
            "delivery_address": "456 Test Ave",
            "phone_number": "0987654321",
            "items": [
                {"menu_item_id": item_id, "quantity": 1}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    response = client.get(
        "/orders",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0

def test_get_order():
    item_id, token = create_menu_item()
    
    # Create an order
    create_response = client.post(
        "/orders",
        json={
            "delivery_address": "789 Test Blvd",
            "phone_number": "5555555555",
            "items": [
                {"menu_item_id": item_id, "quantity": 3}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    order_id = create_response.json()["id"]
    
    response = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert data["total_amount"] == 47.97

def test_update_order():
    item_id, token = create_menu_item()
    
    # Create an order
    create_response = client.post(
        "/orders",
        json={
            "delivery_address": "321 Test Lane",
            "phone_number": "1111111111",
            "items": [
                {"menu_item_id": item_id, "quantity": 1}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    order_id = create_response.json()["id"]
    
    # Update the order
    response = client.put(
        f"/orders/{order_id}",
        json={"status": "confirmed"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"

def test_delete_order():
    item_id, token = create_menu_item()
    
    # Create an order
    create_response = client.post(
        "/orders",
        json={
            "delivery_address": "654 Test Road",
            "phone_number": "2222222222",
            "items": [
                {"menu_item_id": item_id, "quantity": 1}
            ]
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    order_id = create_response.json()["id"]
    
    # Delete the order
    response = client.delete(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404 