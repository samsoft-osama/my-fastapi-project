#!/usr/bin/env python3
"""
Migration script to help transition from old structure to new structure
"""
import os
import shutil
import sys
from pathlib import Path


def backup_old_files():
    """Backup old files before migration"""
    backup_dir = Path("backup_old_structure")
    backup_dir.mkdir(exist_ok=True)
    
    old_files = [
        "main.py",
        "database.py", 
        "models.py",
        "schemas.py",
        "crud.py",
        "auth.py",
        "dependencies.py",
        "config.py",
        "setup_postgres.py"
    ]
    
    for file in old_files:
        if Path(file).exists():
            shutil.copy2(file, backup_dir / file)
            print(f"✅ Backed up {file}")
    
    print(f"📁 Old files backed up to {backup_dir}")


def create_missing_directories():
    """Create missing directories in new structure"""
    directories = [
        "app/utils",
        "scripts",
        "docs",
        "deployments",
        "alembic/versions"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")


def update_imports_in_tests():
    """Update import statements in test files"""
    test_files = [
        "tests/test_auth.py",
        "tests/test_menu.py", 
        "tests/test_orders.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            with open(test_file, 'r') as f:
                content = f.read()
            
            # Update imports
            content = content.replace("from database import", "from app.db.base import")
            content = content.replace("from models import", "from app.models import")
            content = content.replace("from schemas import", "from app.schemas import")
            content = content.replace("from crud import", "from app.services import")
            content = content.replace("from auth import", "from app.core.security import")
            content = content.replace("from config import", "from app.core.config import")
            
            with open(test_file, 'w') as f:
                f.write(content)
            
            print(f"✅ Updated imports in {test_file}")


def create_alembic_env():
    """Create Alembic environment"""
    try:
        import alembic
        os.system("alembic init alembic")
        print("✅ Created Alembic environment")
    except ImportError:
        print("⚠️  Alembic not installed. Run: pip install alembic")


def main():
    """Main migration function"""
    print("🔄 Starting structure migration...")
    
    # Backup old files
    backup_old_files()
    
    # Create missing directories
    create_missing_directories()
    
    # Update test imports
    update_imports_in_tests()
    
    # Create Alembic environment
    create_alembic_env()
    
    print("\n✅ Migration completed!")
    print("\n📋 Next steps:")
    print("1. Review the new structure in the 'app/' directory")
    print("2. Update your .env file with proper configuration")
    print("3. Run 'make install-dev' to install dependencies")
    print("4. Run 'make setup-db' to create database tables")
    print("5. Run 'make run' to start the application")
    print("\n📁 Old files are backed up in 'backup_old_structure/' directory")


if __name__ == "__main__":
    main() 