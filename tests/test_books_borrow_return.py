
"""Tests for borrowing and returning books."""

from flask.testing import FlaskClient


def create_test_book(client: FlaskClient) -> None:
    """Create a sample book for testing."""
    client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
        },
    )


def test_borrow_available_book(client: FlaskClient) -> None:
    """Check that an available book can be borrowed."""
    create_test_book(client)

    response = client.post("/books/1/borrow")

    assert response.status_code == 200
    assert response.get_json()["available"] is False


def test_borrow_book_twice(client: FlaskClient) -> None:
    """Check that an already borrowed book cannot be borrowed again."""
    create_test_book(client)
    client.post("/books/1/borrow")

    response = client.post("/books/1/borrow")

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "CONFLICT"


def test_return_borrowed_book(client: FlaskClient) -> None:
    """Check that a borrowed book can be returned."""
    create_test_book(client)
    client.post("/books/1/borrow")

    response = client.post("/books/1/return")

    assert response.status_code == 200
    assert response.get_json()["available"] is True


def test_return_available_book(client: FlaskClient) -> None:
    """Check that an available book cannot be returned again."""
    create_test_book(client)

    response = client.post("/books/1/return")

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "CONFLICT"


def test_borrow_nonexistent_book(client: FlaskClient) -> None:
    """Check that borrowing a nonexistent book returns 404."""
    response = client.post("/books/99/borrow")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"


def test_return_nonexistent_book(client: FlaskClient) -> None:
    """Check that returning a nonexistent book returns 404."""
    response = client.post("/books/99/return")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"
