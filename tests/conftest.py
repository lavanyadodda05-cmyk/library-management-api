"""Shared fixtures for library API tests."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from flask.testing import FlaskClient

import app.database as database
from app.main import create_app
from app.services.book_service import book_repository


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> Iterator[FlaskClient]:
    """Create a test client using a temporary database."""

    test_database = tmp_path / "test_library.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_database)

    app = create_app()
    app.config.update(TESTING=True)

    book_repository.reset()

    with app.test_client() as test_client:
        yield test_client

    book_repository.reset()
