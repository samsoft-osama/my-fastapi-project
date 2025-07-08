"""
Updated menu tests for the new modular structure
"""
import pytest
from fastapi import status


def test_create_menu_item(client, auth_headers):
    """Test creating a menu item"""
    menu_data = {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato and mozzarella",
        "price": 12.99,
        "category": "Pizza",
        "image_url": "https://example.com/pizza.jpg"
    }
    
    response = client.post("/api/v1/menu/", json=menu_data, headers=auth_headers)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["name"] == menu_data["name"]
    assert data["price"] == menu_data["price"]
    assert data["category"] == menu_data["category"]
    assert data["is_available"] == True  # Default value


def test_get_menu_items(client):
    """Test getting all menu items"""
    response = client.get("/api/v1/menu/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)


def test_get_menu_item(client, auth_headers):
    """Test getting a specific menu item"""
    # Create a menu item first
    menu_data = {
        "name": "Pepperoni Pizza",
        "description": "Pizza with pepperoni toppings",
        "price": 14.99,
        "category": "Pizza"
    }
    
    create_response = client.post("/api/v1/menu/", json=menu_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Get the item
    response = client.get(f"/api/v1/menu/{item_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["name"] == menu_data["name"]
    assert data["price"] == menu_data["price"]


def test_get_nonexistent_menu_item(client):
    """Test getting a menu item that doesn't exist"""
    response = client.get("/api/v1/menu/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_menu_item(client, auth_headers):
    """Test updating a menu item"""
    # Create a menu item
    menu_data = {
        "name": "Veggie Pizza",
        "description": "Vegetarian pizza",
        "price": 11.99,
        "category": "Pizza"
    }
    
    create_response = client.post("/api/v1/menu/", json=menu_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Update the item
    update_data = {
        "price": 13.99,
        "description": "Updated vegetarian pizza description"
    }
    
    response = client.put(f"/api/v1/menu/{item_id}", json=update_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["price"] == update_data["price"]
    assert data["description"] == update_data["description"]


def test_delete_menu_item(client, auth_headers):
    """Test deleting a menu item"""
    # Create a menu item
    menu_data = {
        "name": "Chicken Wings",
        "description": "Spicy chicken wings",
        "price": 8.99,
        "category": "Appetizer"
    }
    
    create_response = client.post("/api/v1/menu/", json=menu_data, headers=auth_headers)
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/menu/{item_id}", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/menu/{item_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_get_menu_by_category(client, auth_headers):
    """Test getting menu items by category"""
    # Create items in different categories
    items = [
        {"name": "Pizza 1", "description": "Pizza", "price": 12.99, "category": "Pizza"},
        {"name": "Pizza 2", "description": "Another pizza", "price": 13.99, "category": "Pizza"},
        {"name": "Burger", "description": "Beef burger", "price": 9.99, "category": "Main Course"}
    ]
    
    for item in items:
        client.post("/api/v1/menu/", json=item, headers=auth_headers)
    
    # Get pizza items
    response = client.get("/api/v1/menu/category/Pizza")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 2
    for item in data:
        assert item["category"] == "Pizza"


def test_search_menu_items(client, auth_headers):
    """Test searching menu items"""
    # Create items with searchable names
    items = [
        {"name": "Chicken Pizza", "description": "Pizza with chicken", "price": 15.99, "category": "Pizza"},
        {"name": "Beef Burger", "description": "Beef burger", "price": 10.99, "category": "Main Course"},
        {"name": "Chicken Wings", "description": "Chicken wings", "price": 8.99, "category": "Appetizer"}
    ]
    
    for item in items:
        client.post("/api/v1/menu/", json=item, headers=auth_headers)
    
    # Search for chicken items
    response = client.get("/api/v1/menu/search/chicken")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) >= 2
    for item in data:
        assert "chicken" in item["name"].lower()


def test_menu_item_validation(client, auth_headers):
    """Test menu item validation"""
    # Test with invalid price
    invalid_data = {
        "name": "Test Item",
        "description": "Test description",
        "price": -5.99,  # Negative price
        "category": "Test"
    }
    
    response = client.post("/api/v1/menu/", json=invalid_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test with empty name
    invalid_data = {
        "name": "",  # Empty name
        "description": "Test description",
        "price": 5.99,
        "category": "Test"
    }
    
    response = client.post("/api/v1/menu/", json=invalid_data, headers=auth_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY 