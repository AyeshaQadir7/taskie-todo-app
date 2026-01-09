# Todo Backend API

A FastAPI-based backend service for multi-user todo task management with persistent storage in Neon Serverless PostgreSQL.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL or Neon serverless database
- Virtual environment (optional but recommended)

### Setup

1. **Create virtual environment**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and set:
# - DATABASE_URL (your PostgreSQL connection string)
# - BETTER_AUTH_SECRET (shared JWT secret)
```

4. **Run migrations** (if using Alembic):
```bash
alembic upgrade head
```

5. **Start the server**:
```bash
python -m uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## Endpoints

### Create Task
POST /api/{user_id}/tasks

### List All Tasks
GET /api/{user_id}/tasks
GET /api/{user_id}/tasks?status=incomplete

### Get Single Task
GET /api/{user_id}/tasks/{id}

### Update Task
PUT /api/{user_id}/tasks/{id}

### Delete Task
DELETE /api/{user_id}/tasks/{id}

### Mark Task Complete
PATCH /api/{user_id}/tasks/{id}/complete

## Testing

```bash
pytest tests/ -v
pytest tests/ --cov=src
```

## Project Structure

```
backend/
├── main.py                  # FastAPI application
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── alembic.ini             # Alembic config
├── alembic/                # Database migrations
├── src/
│   ├── database.py         # Database connection
│   ├── models.py           # SQLModel definitions
│   ├── schemas.py          # Pydantic models
│   ├── services.py         # Business logic
│   └── api/tasks.py        # Endpoints
└── tests/                   # Test suite
```

## Features

- User ownership enforcement on all operations
- Input validation (title: 1-255 chars, description: 5000 max)
- Timestamps (created_at immutable, updated_at auto-updated)
- Consistent error responses with JSON format
- Appropriate HTTP status codes
- Multi-user isolation (users can only see their own tasks)

## Authentication

User ID is passed in the URL path. JWT middleware will be added in a future release.

## License

MIT
