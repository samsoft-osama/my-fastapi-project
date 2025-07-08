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
- 🔄 **Database Migrations** - Alembic for database schema management
- 🛡️ **Security Features** - Input validation, CORS, and security headers

## 🏗️ Project Structure

```
food_order_system/
├── 📁 app/                          # Main application package
│   ├── 📁 api/                      # API layer
│   │   └── 📁 v1/                   # API version 1
│   │       └── 📁 endpoints/        # API endpoints
│   │           ├── 📄 auth.py       # Authentication endpoints
│   │           ├── 📄 users.py      # User management endpoints
│   │           ├── 📄 menu.py       # Menu item endpoints
│   │           └── 📄 orders.py     # Order management endpoints
│   ├── 📁 core/                     # Core application logic
│   │   ├── 📄 config.py             # Configuration settings
│   │   └── 📄 security.py           # Security utilities
│   ├── 📁 db/                       # Database layer
│   │   └── 📄 base.py               # Database configuration
│   ├── 📁 models/                   # Database models
│   │   ├── 📄 user.py               # User model
│   │   ├── 📄 menu_item.py          # Menu item model
│   │   ├── 📄 order.py              # Order model
│   │   └── 📄 order_item.py         # Order item model
│   ├── 📁 schemas/                  # Pydantic schemas
│   │   ├── 📄 user.py               # User schemas
│   │   ├── 📄 auth.py               # Authentication schemas
│   │   ├── 📄 menu.py               # Menu item schemas
│   │   └── 📄 order.py              # Order schemas
│   ├── 📁 services/                 # Business logic layer
│   │   ├── 📄 user_service.py       # User business logic
│   │   ├── 📄 menu_service.py       # Menu business logic
│   │   └── 📄 order_service.py      # Order business logic
│   ├── 📁 utils/                    # Utility functions
│   ├── 📄 main.py                   # FastAPI application
│   └── 📄 __init__.py               # App package init
├── 📁 alembic/                      # Database migrations
├── 📁 scripts/                      # Utility scripts
├── 📁 docs/                         # Documentation
├── 📁 deployments/                  # Deployment configurations
├── 📄 main.py                       # Application entry point
├── 📄 requirements.txt              # Python dependencies
├── 📄 pyproject.toml                # Modern Python project config
├── 📄 Makefile                      # Development tasks
├── 📄 .pre-commit-config.yaml       # Pre-commit hooks
├── 📄 alembic.ini                   # Alembic configuration
├── 📄 .gitignore                    # Git ignore rules
└── 📄 README.md                     # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **PostgreSQL 12+**
- **Make** (optional, for using Makefile commands)

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd food_order_system

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
make install-dev
# Or manually: pip install -e ".[dev,test]"
```

### 2. Database Setup

```bash
# Start PostgreSQL (if not running)
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb food_orders_db

# Setup database tables
make setup-db
```

### 3. Environment Configuration

Create a `.env` file in the project root:
```bash
# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_orders_db

# JWT Configuration
SECRET_KEY=your-very-secure-secret-key-at-least-32-characters-long
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]
```

### 4. Run the Application

```bash
# Run with Makefile
make run

# Or manually
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Access the Application

- 🌐 **API Documentation (Swagger UI)**: http://localhost:8000/docs
- 📖 **Alternative Documentation (ReDoc)**: http://localhost:8000/redoc
- 🏠 **API Root**: http://localhost:8000

## 🛠️ Development

### Available Commands

```bash
# Show all available commands
make help

# Code quality
make format          # Format code with black and isort
make lint            # Run linting checks
make test            # Run tests
make test-cov        # Run tests with coverage

# Database operations
make setup-db        # Create database tables
make migrate         # Create new migration
make migrate-up      # Apply migrations
make migrate-down    # Rollback migrations

# Cleanup
make clean           # Clean cache files
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
pytest tests/test_auth.py -v

# Run with specific markers
pytest -m "not slow"  # Skip slow tests
```

## 📚 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/v1/auth/register` | Register a new user | ❌ |
| `POST` | `/api/v1/auth/token` | Login and get access token | ❌ |
| `POST` | `/api/v1/auth/login` | Login with JSON payload | ❌ |

### 👤 User Management
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/users/me` | Get current user profile | ✅ |
| `PUT` | `/api/v1/users/me` | Update current user | ✅ |
| `DELETE` | `/api/v1/users/me` | Delete current user | ✅ |

### 🍽️ Menu Items
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/menu` | Get all menu items | ❌ |
| `GET` | `/api/v1/menu/{item_id}` | Get specific menu item | ❌ |
| `POST` | `/api/v1/menu` | Create new menu item | ✅ |
| `PUT` | `/api/v1/menu/{item_id}` | Update menu item | ✅ |
| `DELETE` | `/api/v1/menu/{item_id}` | Delete menu item | ✅ |

### 🛒 Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/api/v1/orders` | Get user's orders | ✅ |
| `GET` | `/api/v1/orders/{order_id}` | Get specific order | ✅ |
| `POST` | `/api/v1/orders` | Create new order | ✅ |
| `PUT` | `/api/v1/orders/{order_id}` | Update order | ✅ |
| `DELETE` | `/api/v1/orders/{order_id}` | Delete order | ✅ |

## 🗄️ Database Schema

### 👤 Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    image_url VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    notes TEXT,
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
| `DEBUG` | Debug mode | `False` |
| `CORS_ORIGINS` | Allowed CORS origins | `["http://localhost:3000"]` |

### Production Configuration

For production deployment:

1. **Change the SECRET_KEY** to a strong, random string
2. **Set DEBUG=False**
3. **Use environment variables** for all sensitive configuration
4. **Set up proper PostgreSQL credentials**
5. **Enable HTTPS** for secure communication
6. **Configure CORS** for your frontend domain

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test categories
pytest tests/test_auth.py -v
pytest tests/test_menu.py -v
pytest tests/test_orders.py -v
```

### Test Structure
```
tests/
├── 📁 conftest.py           # Test configuration and fixtures
├── 📁 test_auth.py          # Authentication tests
├── 📁 test_menu.py          # Menu item tests
├── 📁 test_orders.py        # Order management tests
└── 📁 test_integration.py   # Integration tests
```

## 🚀 Deployment

### Environment Setup for Production
```bash
# Set production environment variables
export DB_USER=your_production_user
export DB_PASSWORD=your_secure_password
export DB_HOST=your_production_host
export DB_NAME=your_production_db
export SECRET_KEY=your_very_secure_secret_key
export DEBUG=false
export ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Production Server Setup
```bash
# Install production dependencies
pip install -r requirements.txt

# Run with production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🛡️ Security Features

- **🔐 Password Hashing** - Bcrypt encryption for user passwords
- **🎫 JWT Authentication** - Secure token-based authentication
- **✅ Input Validation** - Pydantic schemas for request validation
- **🛡️ SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **🔒 CORS Support** - Configurable CORS for frontend integration
- **⏰ Token Expiration** - Configurable JWT token expiration
- **🔍 Security Headers** - Automatic security headers
- **🛡️ Rate Limiting** - Configurable rate limiting (optional)

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
   make install-dev
   
   # Activate virtual environment
   source venv/bin/activate
   ```

3. **Database Migration Issues**
   ```bash
   # Reset migrations
   alembic downgrade base
   alembic upgrade head
   ```

4. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Kill the process
   kill -9 <PID>
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`make install-dev`)
4. Set up pre-commit hooks (`pre-commit install`)
5. Make your changes
6. Run tests (`make test`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests
- Update documentation
- Use conventional commit messages
- Run pre-commit hooks before committing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/food-order-system/issues)
- 📖 **Documentation**: [API Docs](http://localhost:8000/docs)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/food-order-system/discussions)

## 🙏 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **PostgreSQL** - Advanced open-source database
- **Pydantic** - Data validation using Python type annotations
- **Alembic** - Database migration tool

---

**Made with ❤️ for the food ordering industry** 