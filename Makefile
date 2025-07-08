# Makefile for Food Order Booking System
# Development and deployment tasks

.PHONY: help install install-dev test test-cov format lint clean setup-db migrate migrate-up migrate-down run

# Default target
help:
	@echo "🍕 Food Order Booking System - Available Commands:"
	@echo ""
	@echo "📦 Installation:"
	@echo "  install      - Install production dependencies"
	@echo "  install-dev  - Install development dependencies"
	@echo ""
	@echo "🧪 Testing:"
	@echo "  test         - Run all tests"
	@echo "  test-cov     - Run tests with coverage"
	@echo ""
	@echo "🎨 Code Quality:"
	@echo "  format       - Format code with black and isort"
	@echo "  lint         - Run linting checks"
	@echo ""
	@echo "🗄️ Database:"
	@echo "  setup-db     - Create database tables"
	@echo "  migrate      - Create new migration"
	@echo "  migrate-up   - Apply migrations"
	@echo "  migrate-down - Rollback migrations"
	@echo ""
	@echo "🚀 Development:"
	@echo "  run          - Run development server"
	@echo ""
	@echo "🧹 Cleanup:"
	@echo "  clean        - Clean cache files"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -e ".[dev,test]"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

# Code Quality
format:
	black app/ tests/ scripts/
	isort app/ tests/ scripts/

lint:
	flake8 app/ tests/ scripts/
	black --check app/ tests/ scripts/
	isort --check-only app/ tests/ scripts/
	mypy app/

# Database Operations
setup-db:
	python -c "from app.db.base import create_tables; create_tables()"

migrate:
	alembic revision --autogenerate -m "$(message)"

migrate-up:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

# Development
run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .mypy_cache/ 