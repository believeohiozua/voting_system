# Feature Voting System - Makefile
# ================================

.PHONY: help install setup backend mobile docker-db docker-backend clean test lint format

# Default target
help:
	@echo "Feature Voting System - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup Commands:"
	@echo "  make install        - Install all dependencies"
	@echo "  make setup          - Complete project setup"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make superuser      - Create Django superuser"
	@echo "  make sample-data    - Create sample feature data"
	@echo ""
	@echo "Development Commands:"
	@echo "  make backend        - Start Django development server"
	@echo "  make mobile         - Start React Native Android app"
	@echo "  make docker-db      - Start PostgreSQL with Docker"
	@echo "  make docker-backend - Start full backend with Docker"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean          - Clean up generated files"
	@echo "  make test           - Run all tests"
	@echo "  make lint           - Run code linting"
	@echo "  make format         - Format code"
	@echo "  make logs           - Show Docker logs"
	@echo ""
	@echo "Quick Start:"
	@echo "  make setup && make docker-db && make backend"

# Installation commands
install:
	@echo "📦 Installing dependencies..."
	@echo "Installing Python dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing Node.js dependencies..."
	cd mobile && npm install
	@echo "✅ All dependencies installed!"

setup: install
	@echo "🚀 Setting up project..."
	@echo "Running Django migrations..."
	cd backend/src && python manage.py makemigrations
	cd backend/src && python manage.py migrate
	@echo "✅ Project setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Run 'make superuser' to create an admin user"
	@echo "2. Run 'make docker-db' to start the database"
	@echo "3. Run 'make backend' to start the Django server"

migrate:
	@echo "🔄 Running Django migrations..."
	cd backend/src && python manage.py makemigrations
	cd backend/src && python manage.py migrate
	@echo "✅ Migrations complete!"

superuser:
	@echo "👤 Creating Django superuser..."
	cd backend/src && python manage.py createsuperuser

sample-data:
	@echo "📊 Creating sample feature data..."
	cd backend/src && python manage.py create_sample_data
	@echo "✅ Sample data created!"

# Development commands
backend:
	@echo "🚀 Starting Django development server..."
	@echo "API will be available at: http://localhost:8000/api/"
	@echo "Swagger docs at: http://localhost:8000/"
	@echo "Admin interface at: http://localhost:8000/admin/"
	@echo ""
	cd backend/src && python manage.py runserver

mobile:
	@echo "📱 Starting React Native Android app..."
	@echo "Make sure you have Android emulator running or device connected"
	cd mobile && npx react-native run-android

# Docker commands
docker-db:
	@echo "🐳 Starting PostgreSQL database with Docker..."
	cd backend && docker-compose up -d db
	@echo "✅ Database started! Connection: localhost:5432"

docker-backend:
	@echo "🐳 Starting full backend stack with Docker..."
	cd backend && docker-compose up

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	cd backend && docker-compose down

docker-logs:
	@echo "📋 Showing Docker logs..."
	cd backend && docker-compose logs -f

# Testing commands
test:
	@echo "🧪 Running tests..."
	@echo "Running Django tests..."
	cd backend/src && python manage.py test
	@echo "Running React Native tests..."
	cd mobile && npm test
	@echo "✅ All tests completed!"

test-backend:
	@echo "🧪 Running Django tests..."
	cd backend/src && python manage.py test

test-mobile:
	@echo "🧪 Running React Native tests..."
	cd mobile && npm test

# Code quality commands
lint:
	@echo "🔍 Running code linting..."
	@echo "Linting Python code..."
	cd backend && python -m flake8 src/ --max-line-length=88 --exclude=migrations || true
	@echo "Linting JavaScript code..."
	cd mobile && npx eslint . --ext .js,.jsx,.ts,.tsx || true
	@echo "✅ Linting complete!"

format:
	@echo "✨ Formatting code..."
	@echo "Formatting Python code with black..."
	cd backend && python -m black src/ || echo "Install black: pip install black"
	@echo "Formatting JavaScript code with prettier..."
	cd mobile && npx prettier --write . || echo "Prettier not configured"
	@echo "✅ Code formatting complete!"

# Utility commands
clean:
	@echo "🧹 Cleaning up generated files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + || true
	cd mobile && rm -rf node_modules/.cache || true
	@echo "✅ Cleanup complete!"

reset-db:
	@echo "🗑️  Resetting database..."
	cd backend && docker-compose down -v
	cd backend/src && rm -f db.sqlite3
	make docker-db
	sleep 5
	make migrate
	@echo "✅ Database reset complete!"

# Development workflow shortcuts
dev: docker-db backend

full-setup: setup superuser sample-data
	@echo "🎉 Full setup complete!"
	@echo ""
	@echo "Your Feature Voting System is ready!"
	@echo "Run 'make dev' to start development"

# Status and info commands
status:
	@echo "📊 Project Status"
	@echo "================"
	@echo ""
	@echo "Docker containers:"
	cd backend && docker-compose ps || echo "Docker not running"
	@echo ""
	@echo "Python environment:"
	which python || echo "Python not found"
	python --version || echo "Python not available"
	@echo ""
	@echo "Node.js environment:"
	which node || echo "Node.js not found"
	node --version || echo "Node.js not available"
	@echo ""
	@echo "Project structure:"
	@ls -la

info:
	@echo "ℹ️  Feature Voting System Information"
	@echo "===================================="
	@echo ""
	@echo "🔗 URLs:"
	@echo "  API Documentation: http://localhost:8000/"
	@echo "  Admin Interface:   http://localhost:8000/admin/"
	@echo "  API Endpoints:     http://localhost:8000/api/"
	@echo ""
	@echo "📱 Mobile:"
	@echo "  React Native Android app connects to: http://10.0.2.2:8000"
	@echo ""
	@echo "🗄️  Database:"
	@echo "  PostgreSQL running on: localhost:5432"
	@echo "  Database name: feature_voting"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  backend/src/     - Django application"
	@echo "  mobile/          - React Native app"
	@echo "  backend/docker-compose.yml - Database setup"

# Quick development commands
quick-start: docker-db
	@echo "⚡ Quick starting development environment..."
	@sleep 3
	@make backend

restart: docker-stop docker-db
	@echo "🔄 Restarting services..."
	@sleep 3
	@make backend