
"""Shared fixtures for library API tests."""

from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

from app.main import create_app
from app.services.book_service import book_repository


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Create a test client and reset the book storage."""
    app = create_app()
    app.config.update(TESTING=True)

    book_repository.reset()

    with app.test_client() as test_client:
        yield test_client

    book_repository.reset()
