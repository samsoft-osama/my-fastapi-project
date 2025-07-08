#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Food Booking Order Management System
"""

import os
import sys

def print_banner():
    print("=" * 60)
    print("PostgreSQL Setup for Food Booking Order Management System")
    print("=" * 60)

def check_postgres_installation():
    """Check if PostgreSQL is installed and running"""
    print("\n1. Checking PostgreSQL installation...")
    
    # Check if psql command is available
    if os.system("which psql > /dev/null 2>&1") != 0:
        print("❌ PostgreSQL is not installed or not in PATH")
        print("\nTo install PostgreSQL on Ubuntu/Debian:")
        print("sudo apt update")
        print("sudo apt install postgresql postgresql-contrib")
        print("\nTo install PostgreSQL on CentOS/RHEL:")
        print("sudo yum install postgresql postgresql-server")
        print("sudo postgresql-setup initdb")
        print("sudo systemctl start postgresql")
        return False
    
    print("✅ PostgreSQL is installed")
    return True

def create_database():
    """Create the database and user"""
    print("\n2. Setting up database...")
    
    # Default configuration
    db_name = "food_orders_db"
    db_user = "postgres"
    db_password = "password"
    
    print(f"Database Name: {db_name}")
    print(f"Database User: {db_user}")
    print(f"Database Password: {db_password}")
    
    # Create database
    create_db_cmd = f"createdb -U {db_user} {db_name}"
    print(f"\nRunning: {create_db_cmd}")
    
    if os.system(create_db_cmd) == 0:
        print("✅ Database created successfully")
        return True
    else:
        print("❌ Failed to create database")
        print("\nYou may need to:")
        print("1. Start PostgreSQL service: sudo systemctl start postgresql")
        print("2. Switch to postgres user: sudo -u postgres psql")
        print("3. Create database manually: CREATE DATABASE food_orders_db;")
        return False

def create_env_file():
    """Create .env file with database configuration"""
    print("\n3. Creating environment configuration...")
    
    env_content = """# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_orders_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def install_dependencies():
    """Install Python dependencies"""
    print("\n4. Installing Python dependencies...")
    
    if os.system("pip3 install -r requirements.txt") == 0:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        return False

def create_tables():
    """Create database tables"""
    print("\n5. Creating database tables...")
    
    try:
        from database import engine
        from models import Base
        
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    print_banner()
    
    steps = [
        ("Checking PostgreSQL installation", check_postgres_installation),
        ("Creating database", create_database),
        ("Creating environment file", create_env_file),
        ("Installing dependencies", install_dependencies),
        ("Creating database tables", create_tables)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        if step_func():
            success_count += 1
        else:
            print(f"\n❌ Setup failed at: {step_name}")
            break
    
    print("\n" + "=" * 60)
    if success_count == len(steps):
        print("🎉 Setup completed successfully!")
        print("\nTo run the application:")
        print("python3 -m uvicorn main:app --reload")
        print("\nAccess the API documentation at:")
        print("http://localhost:8000/docs")
    else:
        print(f"⚠️  Setup completed with {len(steps) - success_count} errors")
        print("Please fix the errors above and run the setup again")
    print("=" * 60)

if __name__ == "__main__":
    main() 