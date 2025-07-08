# FastAPI Food Booking Order Management System

A comprehensive food ordering and management system built with FastAPI, SQLAlchemy, and JWT authentication using PostgreSQL database.

## Features

- **User Authentication**: JWT-based authentication with user registration and login
- **Menu Management**: CRUD operations for menu items with categories and availability
- **Order Management**: Complete order lifecycle from creation to delivery
- **User Management**: User profiles and order history
- **RESTful API**: Clean, well-documented API endpoints
- **Database**: PostgreSQL database with SQLAlchemy ORM
- **Testing**: Comprehensive test suite with pytest

## Project Structure

```
food_order_system/
├── main.py              # FastAPI application with all endpoints
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy models for database tables
├── schemas.py           # Pydantic schemas for request/response validation
├── crud.py              # CRUD operations for database interactions
├── auth.py              # Authentication and JWT token handling
├── dependencies.py      # FastAPI dependencies for authentication
├── config.py            # Configuration settings
├── setup_postgres.py    # PostgreSQL setup script
├── requirements.txt     # Python dependencies
├── README.md           # Project documentation
└── tests/              # Test suite
    ├── __init__.py
    ├── test_auth.py    # Authentication tests
    ├── test_menu.py    # Menu item tests
    └── test_orders.py  # Order management tests
```

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

## Installation

### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**CentOS/RHEL:**
```bash
sudo yum install postgresql postgresql-server
sudo postgresql-setup initdb
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

### 2. Clone the Repository
```bash
git clone <repository-url>
cd food_order_system
```

### 3. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup PostgreSQL Database

**Option A: Use the setup script (Recommended)**
```bash
python3 setup_postgres.py
```

**Option B: Manual setup**
```bash
# Connect to PostgreSQL as postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE food_orders_db;
CREATE USER food_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE food_orders_db TO food_user;
\q
```

### 6. Configure Environment Variables

Create a `.env` file in the project root:
```bash
# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_orders_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 7. Create Database Tables
```bash
python3 -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine); print('Tables created successfully!')"
```

## Running the Application

1. Start the FastAPI server:
```bash
python3 -m uvicorn main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get access token
- `GET /users/me` - Get current user profile

### Menu Items
- `GET /menu` - Get all menu items
- `GET /menu/{item_id}` - Get specific menu item
- `POST /menu` - Create new menu item (authenticated)
- `PUT /menu/{item_id}` - Update menu item (authenticated)
- `DELETE /menu/{item_id}` - Delete menu item (authenticated)

### Orders
- `GET /orders` - Get user's orders (authenticated)
- `GET /orders/{order_id}` - Get specific order (authenticated)
- `POST /orders` - Create new order (authenticated)
- `PUT /orders/{order_id}` - Update order (authenticated)
- `DELETE /orders/{order_id}` - Delete order (authenticated)

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `hashed_password`: Encrypted password
- `is_active`: Account status
- `created_at`: Registration timestamp

### MenuItem
- `id`: Primary key
- `name`: Item name
- `description`: Item description
- `price`: Item price
- `category`: Item category
- `is_available`: Availability status
- `created_at`: Creation timestamp

### Order
- `id`: Primary key
- `user_id`: Foreign key to User
- `total_amount`: Order total
- `status`: Order status (pending, confirmed, preparing, delivered, cancelled)
- `delivery_address`: Delivery address
- `phone_number`: Contact phone number
- `created_at`: Order creation timestamp
- `updated_at`: Last update timestamp

### OrderItem
- `id`: Primary key
- `order_id`: Foreign key to Order
- `menu_item_id`: Foreign key to MenuItem
- `quantity`: Item quantity
- `price`: Item price at time of order

## Usage Examples

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "john_doe",
       "email": "john@example.com",
       "password": "securepassword123"
     }'
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=john_doe&password=securepassword123"
```

### 3. Create a Menu Item
```bash
curl -X POST "http://localhost:8000/menu" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Margherita Pizza",
       "description": "Classic pizza with tomato and mozzarella",
       "price": 12.99,
       "category": "Pizza"
     }'
```

### 4. Create an Order
```bash
curl -X POST "http://localhost:8000/orders" \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "delivery_address": "123 Main St, City, State",
       "phone_number": "1234567890",
       "items": [
         {
           "menu_item_id": 1,
           "quantity": 2
         }
       ]
     }'
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Run specific test files:
```bash
pytest tests/test_auth.py
pytest tests/test_menu.py
pytest tests/test_orders.py
```

## Security Features

- **Password Hashing**: Passwords are hashed using bcrypt
- **JWT Authentication**: Secure token-based authentication
- **Input Validation**: Pydantic schemas for request validation
- **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection
- **CORS Support**: Configurable CORS for frontend integration

## Configuration

### Environment Variables
- `DB_USER`: PostgreSQL username (default: postgres)
- `DB_PASSWORD`: PostgreSQL password (default: password)
- `DB_HOST`: PostgreSQL host (default: localhost)
- `DB_PORT`: PostgreSQL port (default: 5432)
- `DB_NAME`: Database name (default: food_orders_db)
- `SECRET_KEY`: JWT secret key (change in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

### Database Configuration
The system uses PostgreSQL by default. You can modify the database configuration in `config.py` or by setting environment variables.

## Troubleshooting

### Common Issues

1. **PostgreSQL Connection Error**
   - Ensure PostgreSQL is running: `sudo systemctl status postgresql`
   - Check if the database exists: `psql -U postgres -l`
   - Verify credentials in `.env` file

2. **Permission Denied**
   - Make sure the PostgreSQL user has proper permissions
   - Check if the database exists and is accessible

3. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Activate the virtual environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository. 