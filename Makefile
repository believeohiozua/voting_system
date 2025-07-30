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
	@echo "  make backend        - Start Django development server (in container)"
	@echo "  make mobile         - Start React Native Android app"
	@echo "  make mobile-setup   - Setup React Native Android environment"
	@echo "  make docker-db      - Start PostgreSQL with Docker"
	@echo "  make docker-backend - Start full backend with Docker"
	@echo "  make docker-shell   - Open shell in backend container"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean          - Clean up generated files"
	@echo "  make test           - Run all tests (in containers)"
	@echo "  make test-schema    - Test OpenAPI schema generation"
	@echo "  make docker-logs    - Show all Docker logs"
	@echo "  make docker-logs-backend - Show backend logs"
	@echo "  make docker-logs-db - Show database logs"
	@echo ""
	@echo "Quick Start:"
	@echo "  make setup && make backend"

# Installation commands
install:
	@echo "📦 Installing dependencies..."
	@echo "Installing Python dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing Node.js dependencies..."
	cd mobile && npm install
	@echo "✅ All dependencies installed!"

setup: install docker-db
	@echo "🚀 Setting up project..."
	@echo "Creating environment file..."
	@if [ ! -f backend/.env ]; then \
		cp backend/.env.example backend/.env; \
		echo "Created backend/.env from example"; \
	fi
	@echo "Waiting for database to be ready..."
	@sleep 5
	@echo "Running Django migrations..."
	make migrate
	@echo "✅ Project setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Run 'make superuser' to create an admin user"
	@echo "2. Run 'make sample-data' to create sample data"
	@echo "3. Run 'make backend' to start the Django server"

migrate:
	@echo "🔄 Running Django migrations..."
	docker compose exec backend python manage.py makemigrations
	docker compose exec backend python manage.py migrate
	@echo "✅ Migrations complete!"

superuser:
	@echo "👤 Creating Django superuser..."
	cd backend && docker compose exec backend python manage.py createsuperuser

sample-data:
	@echo "📊 Creating sample feature data..."
	cd backend && docker compose exec backend python manage.py create_sample_data
	@echo "✅ Sample data created!"

# Development commands
backend:
	@echo "🚀 Starting Django development server..."
	@echo "API will be available at: http://localhost:8000/api/"
	@echo "Swagger docs at: http://localhost:8000/"
	@echo "Admin interface at: http://localhost:8000/admin/"
	@echo ""
	cd backend && docker compose exec backend python manage.py runserver 0.0.0.0:8000

mobile:
	@echo "📱 Starting React Native Android app..."
	@echo "Make sure you have Android emulator running or device connected"
	@if [ ! -f mobile/android/app/debug.keystore ]; then \
		echo "Generating debug keystore..."; \
		cd mobile/android && ./generate-keystore.sh; \
	fi
	cd mobile && npx react-native run-android

mobile-setup:
	@echo "🔧 Setting up React Native Android..."
	cd mobile && npm install
	cd mobile/android && ./generate-keystore.sh
	@echo "✅ Mobile setup complete!"

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

docker-shell:
	@echo "🐚 Opening shell in backend container..."
	cd backend && docker compose exec backend bash

docker-logs-backend:
	@echo "📋 Showing backend logs..."
	cd backend && docker-compose logs -f backend

docker-logs-db:
	@echo "📋 Showing database logs..."
	cd backend && docker-compose logs -f db

docker-ps:
	@echo "📊 Docker container status..."
	cd backend && docker-compose ps

# Testing commands
test:
	@echo "🧪 Running tests..."
	@echo "Running Django tests..."
	cd backend && docker compose exec backend python manage.py test
	@echo "Running React Native tests..."
	cd mobile && npm test
	@echo "✅ All tests completed!"

test-backend:
	@echo "🧪 Running Django tests..."
	cd backend && docker compose exec backend python manage.py test

test-mobile:
	@echo "🧪 Running React Native tests..."
	cd mobile && npm test

test-schema:
	@echo "🧪 Testing OpenAPI schema generation..."
	cd backend && docker compose exec backend python manage.py test_schema



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
dev: docker-db
	@echo "⚡ Starting development environment..."
	@sleep 3
	@make backend

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
	@echo "  DATABASE_URL: postgresql://postgres:password@db:5432/feature_voting"
	@echo ""
	@echo "🔐 Authentication:"
	@echo "  JWT tokens for mobile app authentication"
	@echo "  Register: POST /api/auth/register/"
	@echo "  Login: POST /api/auth/login/"
	@echo ""
	@echo "📁 Project Structure:"
	@echo "  backend/src/     - Django application"
	@echo "  mobile/          - React Native app"
	@echo "  backend/docker-compose.yml - Database setup"

# CI/CD commands
ci-backend:
	@echo "🔄 Running backend CI locally..."
	@echo "Starting database for tests..."
	make docker-db
	@sleep 5
	@echo "Running Django tests..."
	cd backend && docker compose exec backend python manage.py test

ci-mobile:
	@echo "🔄 Running mobile CI locally..."
	cd mobile && npm install
	cd mobile && npm test -- --watchAll=false

ci-all: ci-backend ci-mobile
	@echo "✅ All CI checks passed locally!"

# Quick development commands
quick-start: docker-db
	@echo "⚡ Quick starting development environment..."
	@sleep 3
	@make backend

restart: docker-stop docker-db
	@echo "🔄 Restarting services..."
	@sleep 3
	@make backend