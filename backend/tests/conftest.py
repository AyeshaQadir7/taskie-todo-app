"""Pytest configuration and fixtures for testing"""
import os
from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from src.database import get_session
from src.models import User
from src.auth.jwt_utils import create_test_jwt_token
from main import app


# Create test database URL (SQLite in-memory for speed)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(name="engine")
def engine_fixture():
    """Create test database engine with in-memory SQLite"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine) -> Generator[Session, None, None]:
    """Create test database session"""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_secret")
def test_secret_fixture():
    """Provide test JWT secret for token generation"""
    # Use a fixed secret for testing
    return "test_secret_minimum_32_characters_longggg"


@pytest.fixture(name="client")
def client_fixture(session: Session, test_secret: str) -> Generator[TestClient, None, None]:
    """Create test client with dependency override and JWT authentication"""

    def get_session_override():
        return session

    # Override environment variable for JWT validation
    with patch.dict(os.environ, {"BETTER_AUTH_SECRET": test_secret}):
        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Create a test user"""
    user = User(id="test-user-1", email="test@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user_2")
def test_user_2_fixture(session: Session) -> User:
    """Create a second test user for isolation testing"""
    user = User(id="test-user-2", email="test2@example.com")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_token")
def test_token_fixture(test_user: User, test_secret: str) -> str:
    """Generate valid JWT token for test_user"""
    with patch.dict(os.environ, {"BETTER_AUTH_SECRET": test_secret}):
        return create_test_jwt_token(test_user.id, test_user.email, secret=test_secret)


@pytest.fixture(name="test_token_2")
def test_token_2_fixture(test_user_2: User, test_secret: str) -> str:
    """Generate valid JWT token for test_user_2"""
    with patch.dict(os.environ, {"BETTER_AUTH_SECRET": test_secret}):
        return create_test_jwt_token(test_user_2.id, test_user_2.email, secret=test_secret)


@pytest.fixture(name="authenticated_client")
def authenticated_client_fixture(client: TestClient, test_token: str) -> TestClient:
    """Create test client with JWT authentication headers"""
    # Add default authorization header
    client.headers["Authorization"] = f"Bearer {test_token}"
    return client


@pytest.fixture(name="authenticated_client_2")
def authenticated_client_2_fixture(client: TestClient, test_token_2: str) -> TestClient:
    """Create test client with JWT authentication for second user"""
    client.headers["Authorization"] = f"Bearer {test_token_2}"
    return client
