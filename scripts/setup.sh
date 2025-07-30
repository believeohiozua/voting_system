#!/bin/bash

# Feature Voting System Setup Script
# ==================================

set -e  # Exit on any error

echo "🚀 Feature Voting System Setup"
echo "=============================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed."
    exit 1
fi

echo "✅ All prerequisites found!"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "Installing Python dependencies..."
cd backend && pip install -r requirements.txt
cd ..

echo "Installing Node.js dependencies..."
cd mobile && npm install
cd ..

echo "✅ Dependencies installed!"
echo ""

# Setup Django
echo "🔧 Setting up Django..."
cd backend/src
python manage.py makemigrations
python manage.py migrate
cd ../..

echo "✅ Django setup complete!"
echo ""

# Start database
echo "🐳 Starting PostgreSQL database..."
cd backend && docker-compose up -d db
cd ..

echo "✅ Database started!"
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a superuser: make superuser"
echo "2. Create sample data: make sample-data"
echo "3. Start backend: make backend"
echo "4. Start mobile app: make mobile"
echo ""
echo "Or run: make dev"