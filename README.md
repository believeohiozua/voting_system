# Feature Voting System

A full-stack feature voting application with Django REST API backend and React Native Android frontend.

## Architecture

- **Backend**: Django REST Framework with PostgreSQL
- **Frontend**: React Native for Android
- **Database**: PostgreSQL (containerized with Docker)

## Features

- Create new feature requests
- Upvote existing features
- View features sorted by votes
- Real-time updates

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 16+
- Docker & Docker Compose
- Android Studio (for React Native Android development)
- React Native CLI
- Make (usually pre-installed on macOS/Linux)

### Quick Start

```bash
# Complete setup
make setup

# Create admin user
make superuser

# Create sample data (optional)
make sample-data

# Start development
make dev
```

### Manual Setup

#### Backend Setup

1. Install dependencies and setup:

```bash
make install
make migrate
```

2. Create a superuser:

```bash
make superuser
```

3. Start database and backend:

```bash
make docker-db
make backend
```

#### Mobile App Setup

```bash
make mobile
```

### Available Commands

Run `make help` to see all available commands:

- `make setup` - Complete project setup
- `make backend` - Start Django development server
- `make mobile` - Start React Native Android app
- `make docker-db` - Start PostgreSQL database
- `make test` - Run all tests
- `make clean` - Clean up generated files

### URLs

- **API Documentation**: `http://localhost:8000/` (Swagger UI)
- **Django Admin**: `http://localhost:8000/admin/`
- **API Endpoints**: `http://localhost:8000/api/`

## API Documentation

The API includes interactive Swagger/OpenAPI documentation:

- **Swagger UI**: `http://localhost:8000/` (main landing page)
- **ReDoc**: `http://localhost:8000/redoc/` (alternative documentation)
- **OpenAPI Schema**: `http://localhost:8000/api/schema/` (JSON schema)

## API Endpoints

- `GET /api/features/` - List all features
- `POST /api/features/` - Create a new feature
- `GET /api/features/{id}/` - Get a specific feature
- `PUT /api/features/{id}/` - Update a feature
- `PATCH /api/features/{id}/` - Partially update a feature
- `DELETE /api/features/{id}/` - Delete a feature
- `POST /api/features/{id}/upvote/` - Upvote a feature

## Development Notes

- The Android app uses `10.0.2.2:8000` to connect to localhost Django server
- CORS is enabled for development
- Database runs on port 5432
- Django runs on port 8000

## Project Structure

```
├── backend/                 # Django REST API
│   ├── src/                # Django source code
│   │   ├── feature_voting/ # Django project settings
│   │   ├── features/       # Features app
│   │   └── manage.py       # Django management script
│   ├── docker-compose.yml  # PostgreSQL container
│   ├── Dockerfile          # Docker configuration
│   └── requirements.txt    # Python dependencies
├── mobile/                 # React Native Android app
│   ├── App.tsx            # Main app component
│   ├── android/           # Android-specific files
│   └── package.json       # Node.js dependencies
├── Makefile              # Project automation
├── .gitignore            # Git ignore rules
└── README.md
```
