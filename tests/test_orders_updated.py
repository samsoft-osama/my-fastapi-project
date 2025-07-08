"""
Updated order tests for the new modular structure
"""
import pytest
from fastapi import status


def test_create_order(client, auth_headers):
    """Test creating an order"""
    # First create menu items
    menu_items = [
        {"name": "Pizza", "description": "Delicious pizza", "price": 12.99, "category": "Pizza"},
        {"name": "Burger", "description": "Tasty burger", "price": 8.99, "category": "Main Course"}
    ]
    
    created_items = []
    for item in menu_items:
        response = client.post("/api/v1/menu/", json=item, headers=auth_headers)
        created_items.append(response.json())
    
    # Create order
    order_data = {
        "delivery_address": "123 Main St, City",
        "phone_number": "1234567890",
        "notes": "Extra cheese please",
        "items": [
            {"menu_item_id": created_items[0]["id"], "quantity": 2},
            {"menu_item_id": created_items[1]["id"], "quantity": 1}
        ]
    }
    
    response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["delivery_address"] == order_data["delivery_address"]
    assert data["phone_number"] == order_data["phone_number"]
    assert data["status"] == "pending"
    assert len(data["order_items"]) == 2
    assert data["total_amount"] > 0


def test_get_orders(client, auth_headers):
    """Test getting user orders"""
    response = client.get("/api/v1/orders/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)


def test_get_order(client, auth_headers):
    """Test getting a specific order"""
    # Create an order first
    menu_item = {"name": "Test Pizza", "description": "Test", "price": 10.99, "category": "Pizza"}
    menu_response = client.post("/api/v1/menu/", json=menu_item, headers=auth_headers)
    menu_id = menu_response.json()["id"]
    
    order_data = {
        "delivery_address": "456 Oak St",
        "phone_number": "9876543210",
        "items": [{"menu_item_id": menu_id, "quantity": 1}]
    }
    
    create_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]
    
    # Get the order
    response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == order_id
    assert data["delivery_address"] == order_data["delivery_address"]


def test_get_nonexistent_order(client, auth_headers):
    """Test getting an order that doesn't exist"""
    response = client.get("/api/v1/orders/99999", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_order(client, auth_headers):
    """Test updating an order"""
    # Create an order first
    menu_item = {"name": "Update Pizza", "description": "Test", "price": 11.99, "category": "Pizza"}
    menu_response = client.post("/api/v1/menu/", json=menu_item, headers=auth_headers)
    menu_id = menu_response.json()["id"]
    
    order_data = {
        "delivery_address": "789 Pine St",
        "phone_number": "5551234567",
        "items": [{"menu_item_id": menu_id, "quantity": 1}]
    }
    
    create_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]
    
    # Update the order
    update_data = {
        "delivery_address": "Updated Address",
        "notes": "Updated notes"
    }
    
    response = client.put(f"/api/v1/orders/{order_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["delivery_address"] == update_data["delivery_address"]
    assert data["notes"] == update_data["notes"]


def test_delete_order(client, auth_headers):
    """Test deleting an order"""
    # Create an order first
    menu_item = {"name": "Delete Pizza", "description": "Test", "price": 9.99, "category": "Pizza"}
    menu_response = client.post("/api/v1/menu/", json=menu_item, headers=auth_headers)
    menu_id = menu_response.json()["id"]
    
    order_data = {
        "delivery_address": "Delete Address",
        "phone_number": "1112223333",
        "items": [{"menu_item_id": menu_id, "quantity": 1}]
    }
    
    create_response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    order_id = create_response.json()["id"]
    
    # Delete the order
    response = client.delete(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_order_history(client, auth_headers):
    """Test getting order history"""
    response = client.get("/api/v1/orders/history", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)


def test_order_validation(client, auth_headers):
    """Test order validation"""
    # Test with empty delivery address
    invalid_order = {
        "delivery_address": "",
        "phone_number": "1234567890",
        "items": []
    }
    
    response = client.post("/api/v1/orders/", json=invalid_order, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test with invalid phone number
    invalid_order = {
        "delivery_address": "Valid Address",
        "phone_number": "invalid-phone",
        "items": []
    }
    
    response = client.post("/api/v1/orders/", json=invalid_order, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test with empty items list
    invalid_order = {
        "delivery_address": "Valid Address",
        "phone_number": "1234567890",
        "items": []
    }
    
    response = client.post("/api/v1/orders/", json=invalid_order, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_order_with_invalid_menu_item(client, auth_headers):
    """Test creating order with invalid menu item"""
    order_data = {
        "delivery_address": "Test Address",
        "phone_number": "1234567890",
        "items": [{"menu_item_id": 99999, "quantity": 1}]  # Non-existent menu item
    }
    
    response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    # This should still create the order but with 0 total if menu item doesn't exist
    assert response.status_code == status.HTTP_201_CREATED


def test_order_total_calculation(client, auth_headers):
    """Test order total calculation"""
    # Create menu items with specific prices
    menu_items = [
        {"name": "Item 1", "description": "Test", "price": 10.00, "category": "Test"},
        {"name": "Item 2", "description": "Test", "price": 15.50, "category": "Test"}
    ]
    
    created_items = []
    for item in menu_items:
        response = client.post("/api/v1/menu/", json=item, headers=auth_headers)
        created_items.append(response.json())
    
    # Create order with specific quantities
    order_data = {
        "delivery_address": "Test Address",
        "phone_number": "1234567890",
        "items": [
            {"menu_item_id": created_items[0]["id"], "quantity": 2},  # 2 * 10.00 = 20.00
            {"menu_item_id": created_items[1]["id"], "quantity": 1}   # 1 * 15.50 = 15.50
        ]
    }
    
    response = client.post("/api/v1/orders/", json=order_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    expected_total = 20.00 + 15.50  # 35.50
    assert abs(data["total_amount"] - expected_total) < 0.01  # Allow for floating point precision 