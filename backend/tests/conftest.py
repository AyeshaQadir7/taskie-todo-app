"""Pytest configuration and fixtures for testing"""
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from src.database import get_session
from src.models import User
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


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """Create test client with dependency override"""

    def get_session_override():
        return session

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
