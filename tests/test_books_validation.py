
"""Tests for book input validation and error responses."""

from datetime import date

from flask.testing import FlaskClient
from app.services.book_service import book_service


def test_missing_title(client: FlaskClient) -> None:
    """Reject a book without a title."""
    response = client.post(
        "/books",
        json={"author": "John"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_missing_author(client: FlaskClient) -> None:
    """Reject a book without an author."""
    response = client.post(
        "/books",
        json={"title": "Python Basics"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_isbn_characters(client: FlaskClient) -> None:
    """Reject an ISBN containing letters."""
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
            "isbn": "12345ABCDE",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_isbn_length(client: FlaskClient) -> None:
    """Reject an ISBN with an invalid length."""
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
            "isbn": "12345",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_year_type(client: FlaskClient) -> None:
    """Reject a year that is not an integer."""
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
            "year": "2025",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_future_year(client: FlaskClient) -> None:
    """Reject a year greater than the current year."""
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
            "year": date.today().year + 1,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_duplicate_isbn(client: FlaskClient) -> None:
    """Reject a book with an ISBN that already exists."""
    book = {
        "title": "Python Basics",
        "author": "John",
        "isbn": "1234567890",
    }

    client.post("/books", json=book)
    response = client.post("/books", json=book)

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "CONFLICT"


def test_invalid_available_filter(client: FlaskClient) -> None:
    """Reject an invalid available query parameter."""
    response = client.get("/books?available=yes")

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_json_body(client: FlaskClient) -> None:
    """Reject a request body that is not a JSON object."""
    response = client.post(
        "/books",
        data="invalid json",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_unknown_url_returns_json_error(client: FlaskClient) -> None:
    """Check that an unknown URL returns a JSON 404 error."""
    response = client.get("/unknown-url")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"


def test_method_not_allowed_returns_json_error(
    client: FlaskClient,
) -> None:
    """Check that an unsupported HTTP method returns JSON 405."""
    response = client.post("/health")

    assert response.status_code == 405
    assert response.get_json()["error"]["code"] == "METHOD_NOT_ALLOWED"


def test_unexpected_error_returns_json_error(
    client: FlaskClient,
    monkeypatch,
) -> None:
    """Check that unexpected errors return a safe JSON response."""

    def raise_unexpected_error(book_id: int) -> None:
        raise RuntimeError("Test error")

    monkeypatch.setattr(
        book_service,
        "get_book",
        raise_unexpected_error,
    )

    response = client.get("/books/1")

    assert response.status_code == 500
    assert response.get_json()["error"]["code"] == "INTERNAL_ERROR"
    assert response.get_json()["error"]["message"] == (
        "An unexpected error occurred."
    )

