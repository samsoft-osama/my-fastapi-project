# 🍕 FastAPI Food Booking Order Management System

A modern, scalable food ordering and management system built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. Features JWT authentication, comprehensive API endpoints, and a complete order lifecycle management system.

## ✨ Features

- 🔐 **Secure Authentication** - JWT-based user authentication with password hashing
- 📋 **Menu Management** - Full CRUD operations for menu items with categories
- 🛒 **Order Management** - Complete order lifecycle (pending → confirmed → preparing → delivered)
- 👤 **User Management** - User profiles, order history, and account management
- 🚀 **RESTful API** - Clean, well-documented API endpoints with automatic documentation
- 🗄️ **PostgreSQL Database** - Robust, scalable database with SQLAlchemy ORM
- 🧪 **Comprehensive Testing** - Full test suite with pytest
- 🔧 **Environment Configuration** - Flexible configuration management
- 📚 **Auto-generated Docs** - Interactive API documentation with Swagger UI

## 🏗️ Project Structure

```
food_order_system/
├── 📁 main.py                 # FastAPI application with all endpoints
├── 📁 database.py             # Database configuration and session management
├── 📁 models.py               # SQLAlchemy models for database tables
├── 📁 schemas.py              # Pydantic schemas for request/response validation
├── 📁 crud.py                 # CRUD operations for database interactions
├── 📁 auth.py                 # Authentication and JWT token handling
├── 📁 dependencies.py         # FastAPI dependencies for authentication
├── 📁 config.py               # Configuration settings and environment variables
├── 📁 setup_postgres.py       # PostgreSQL setup automation script
├── 📁 requirements.txt        # Python dependencies
├── 📁 .gitignore              # Git ignore rules
├── 📁 README.md               # Project documentation
└── 📁 tests/                  # Test suite
    ├── 📁 __init__.py
    ├── 📁 test_auth.py        # Authentication tests
    ├── 📁 test_menu.py        # Menu item tests
    └── 📁 test_orders.py      # Order management tests
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+**
- **pip** (Python package manager)

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

### 2. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd food_order_system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

**Option A: Automated Setup (Recommended)**
```bash
python3 setup_postgres.py
```

**Option B: Manual Setup**
```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database
CREATE DATABASE food_orders_db;
\q

# Create tables
python3 -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine); print('✅ Tables created!')"
```

### 4. Environment Configuration

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

### 5. Run the Application

```bash
python3 -m uvicorn main:app --reload
```

Access the application:
- 🌐 **API Documentation (Swagger UI)**: http://localhost:8000/docs
- 📖 **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- 🏠 **API Root**: http://localhost:8000

## 📚 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register` | Register a new user | ❌ |
| `POST` | `/token` | Login and get access token | ❌ |
| `GET` | `/users/me` | Get current user profile | ✅ |

### 🍽️ Menu Items
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/menu` | Get all menu items | ❌ |
| `GET` | `/menu/{item_id}` | Get specific menu item | ❌ |
| `POST` | `/menu` | Create new menu item | ✅ |
| `PUT` | `/menu/{item_id}` | Update menu item | ✅ |
| `DELETE` | `/menu/{item_id}` | Delete menu item | ✅ |

### 🛒 Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/orders` | Get user's orders | ✅ |
| `GET` | `/orders/{order_id}` | Get specific order | ✅ |
| `POST` | `/orders` | Create new order | ✅ |
| `PUT` | `/orders/{order_id}` | Update order | ✅ |
| `DELETE` | `/orders/{order_id}` | Delete order | ✅ |

## 🗄️ Database Schema

### 👤 Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🍽️ Menu Items Table
```sql
CREATE TABLE menu_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🛒 Orders Table
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR DEFAULT 'pending',
    delivery_address TEXT NOT NULL,
    phone_number VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📦 Order Items Table
```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    menu_item_id INTEGER REFERENCES menu_items(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10,2) NOT NULL
);
```

## 💡 Usage Examples

### 1. Register a New User
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

## 🧪 Testing

Run the complete test suite:
```bash
pytest tests/
```

Run specific test categories:
```bash
# Authentication tests
pytest tests/test_auth.py

# Menu management tests
pytest tests/test_menu.py

# Order management tests
pytest tests/test_orders.py
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `DB_USER` | PostgreSQL username | `postgres` |
| `DB_PASSWORD` | PostgreSQL password | `password` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `food_orders_db` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here-change-in-production` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

### Production Configuration

For production deployment, make sure to:

1. **Change the SECRET_KEY** to a strong, random string
2. **Use environment variables** for all sensitive configuration
3. **Set up proper PostgreSQL credentials**
4. **Enable HTTPS** for secure communication
5. **Configure CORS** for your frontend domain

## 🛡️ Security Features

- **🔐 Password Hashing** - Bcrypt encryption for user passwords
- **🎫 JWT Authentication** - Secure token-based authentication
- **✅ Input Validation** - Pydantic schemas for request validation
- **🛡️ SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **🔒 CORS Support** - Configurable CORS for frontend integration
- **⏰ Token Expiration** - Configurable JWT token expiration

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup for Production

```bash
# Set production environment variables
export DB_USER=your_production_user
export DB_PASSWORD=your_secure_password
export DB_HOST=your_production_host
export DB_NAME=your_production_db
export SECRET_KEY=your_very_secure_secret_key
export ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🐛 Troubleshooting

### Common Issues

1. **PostgreSQL Connection Error**
   ```bash
   # Check if PostgreSQL is running
   sudo systemctl status postgresql
   
   # Check database connection
   psql -U postgres -d food_orders_db
   ```

2. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install -r requirements.txt
   
   # Activate virtual environment
   source venv/bin/activate
   ```

3. **Permission Denied**
   ```bash
   # Check PostgreSQL user permissions
   sudo -u postgres psql -c "\du"
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/food-order-system/issues)
- 📖 **Documentation**: [API Docs](http://localhost:8000/docs)

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Advanced open-source database
- **Pydantic** - Data validation using Python type annotations

---

**Made with ❤️ for the food ordering industry** 