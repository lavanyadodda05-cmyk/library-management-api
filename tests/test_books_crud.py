
"""Tests for book creation, retrieval, update, and deletion."""

from flask.testing import FlaskClient


def test_create_book(client: FlaskClient) -> None:
    """Check that a new book can be created."""
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John",
            "isbn": "1234567890",
            "year": 2025,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["title"] == "Python Basics"
    assert response.get_json()["available"] is True


def test_get_all_books(client: FlaskClient) -> None:
    """Check that all books can be retrieved."""
    client.post(
        "/books",
        json={"title": "Python Basics", "author": "John"},
    )

    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_book_by_id(client: FlaskClient) -> None:
    """Check that a book can be retrieved using its ID."""
    client.post(
        "/books",
        json={"title": "Python Basics", "author": "John"},
    )

    response = client.get("/books/1")

    assert response.status_code == 200
    assert response.get_json()["id"] == 1


def test_update_book(client: FlaskClient) -> None:
    """Check that an existing book can be updated."""
    client.post(
        "/books",
        json={"title": "Python Basics", "author": "John"},
    )

    response = client.put(
        "/books/1",
        json={"title": "Advanced Python", "author": "John"},
    )

    assert response.status_code == 200
    assert response.get_json()["title"] == "Advanced Python"


def test_delete_book(client: FlaskClient) -> None:
    """Check that a book can be deleted."""
    client.post(
        "/books",
        json={"title": "Python Basics", "author": "John"},
    )

    response = client.delete("/books/1")

    assert response.status_code == 204
    assert response.data == b""
    assert client.get("/books/1").status_code == 404
