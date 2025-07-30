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
- `make ci-backend` - Run backend CI locally
- `make ci-mobile` - Run mobile CI locally
- `make ci-all` - Run all CI checks locally
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

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login user (returns JWT tokens)
- `GET /api/auth/profile/` - Get user profile (requires auth)
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Features

- `GET /api/features/` - List all features (public)
- `POST /api/features/` - Create a new feature (requires auth)
- `GET /api/features/{id}/` - Get a specific feature (public)
- `PUT /api/features/{id}/` - Update a feature (author only)
- `PATCH /api/features/{id}/` - Partially update a feature (author only)
- `DELETE /api/features/{id}/` - Delete a feature (author only)
- `POST /api/features/{id}/upvote/` - Upvote a feature (requires auth)
- `DELETE /api/features/{id}/remove_vote/` - Remove vote from a feature (requires auth)

## Development Notes

- The Android app uses `10.0.2.2:8000` to connect to localhost Django server
- CORS is enabled for development
- Database runs on port 5432
- Django runs on port 8000
- JWT authentication is used for mobile app
- Users must register/login to create features and vote
- Users can only vote once per feature
- Users cannot vote for their own features
- Only feature authors can update/delete their features

## Environment Configuration

The application uses `DATABASE_URL` for database configuration:

- **Docker**: `postgresql://postgres:password@db:5432/feature_voting`
- **Local**: `postgresql://postgres:password@localhost:5432/feature_voting`

Copy `backend/.env.example` to `backend/.env` and adjust as needed.

## CI/CD Pipeline

The project uses separate GitHub Actions workflows for optimal performance:

### Backend CI (`backend-ci.yml`)

- **Triggers**: Changes to `backend/` directory
- **Jobs**: Test, Lint, Docker Build, Security Scan
- **Database**: PostgreSQL service container
- **Coverage**: Uploaded to Codecov

### Mobile CI (`mobile-ci.yml`)

- **Triggers**: Changes to `mobile/` directory
- **Jobs**: Test, Lint, Build, Android APK (main branch)
- **Node.js**: Version 18 with npm caching
- **Security**: npm audit and vulnerability scanning

### Full CI (`full-ci.yml`)

- **Triggers**: Main branch pushes, manual dispatch
- **Features**: Path-based change detection, integration testing
- **Integration**: End-to-end API and mobile bundle testing

Run CI checks locally:

```bash
make ci-backend  # Backend tests and linting
make ci-mobile   # Mobile tests and linting
make ci-all      # All CI checks
```

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
