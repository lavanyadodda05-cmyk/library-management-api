"""Tests for SQLite book repository edge cases."""

from flask.testing import FlaskClient

from app.services.book_service import book_repository


def test_find_by_isbn_excludes_given_book_id(client: FlaskClient) -> None:
    """Check ISBN search while excluding a specific book ID."""
    book = book_repository.create(
        title="Python Basics",
        author="John",
        isbn="1234567890",
        year=2025,
    )

    result = book_repository.find_by_isbn(
        "1234567890",
        exclude_id=book.id,
    )

    assert result is None


def test_update_nonexistent_book_returns_none(client: FlaskClient) -> None:
    """Check updating a book that does not exist."""
    result = book_repository.update(
        book_id=999,
        title="Updated Python",
        author="John",
        isbn="1234567890",
        year=2025,
    )

    assert result is None


def test_set_availability_nonexistent_book_returns_none(
    client: FlaskClient,
) -> None:
    """Check changing availability for a nonexistent book."""
    result = book_repository.set_availability(
        book_id=999,
        available=False,
    )

    assert result is None
