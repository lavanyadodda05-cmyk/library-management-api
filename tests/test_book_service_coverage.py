"""Additional tests for book service coverage."""

import pytest
from flask.testing import FlaskClient

from app.errors import APIError
from app.services.book_service import book_repository, book_service


def test_title_exceeding_limit_is_rejected(client: FlaskClient) -> None:
    response = client.post(
        "/books",
        json={"title": "T" * 201, "author": "John"},
    )
    assert response.status_code == 400


def test_author_exceeding_limit_is_rejected(client: FlaskClient) -> None:
    response = client.post(
        "/books",
        json={"title": "Python", "author": "A" * 101},
    )
    assert response.status_code == 400


def test_list_books_with_author_and_availability_filters(
    client: FlaskClient,
) -> None:
    book_repository.create("Python", "John", None, None)
    borrowed = book_repository.create("Java", "John", None, None)
    book_repository.set_availability(borrowed.id, False)
    book_repository.create("Python", "David", None, None)

    result = book_service.list_books(author="JOHN", available=False)

    assert len(result) == 1
    assert result[0].id == borrowed.id


def test_update_with_duplicate_isbn_returns_conflict(
    client: FlaskClient,
) -> None:
    first = book_repository.create("Python", "John", "1234567890", None)
    second = book_repository.create("Java", "David", "9876543210", None)

    with pytest.raises(APIError) as error:
        book_service.update_book(
            second.id, "Java", "David", first.isbn
        )

    assert error.value.code == "CONFLICT"


def test_update_repository_failure_returns_not_found(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    book = book_repository.create("Python", "John", None, None)
    monkeypatch.setattr(book_repository, "update", lambda *args: None)

    with pytest.raises(APIError) as error:
        book_service.update_book(book.id, "Advanced Python", "John")

    assert error.value.code == "NOT_FOUND"


def test_delete_nonexistent_book_returns_not_found(
    client: FlaskClient,
) -> None:
    with pytest.raises(APIError) as error:
        book_service.delete_book(999)

    assert error.value.code == "NOT_FOUND"


def test_borrow_repository_failure_returns_not_found(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    book = book_repository.create("Python", "John", None, None)
    monkeypatch.setattr(
        book_repository, "set_availability", lambda *args: None
    )

    with pytest.raises(APIError) as error:
        book_service.borrow_book(book.id)

    assert error.value.code == "NOT_FOUND"


def test_return_repository_failure_returns_not_found(
    client: FlaskClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    book = book_repository.create("Python", "John", None, None)
    book_repository.set_availability(book.id, False)

    monkeypatch.setattr(
        book_repository, "set_availability", lambda *args: None
    )

    with pytest.raises(APIError) as error:
        book_service.return_book(book.id)

    assert error.value.code == "NOT_FOUND"
def test_get_books_with_available_false_filter(client):
    client.post(
        "/books",
        json={"title": "Python", "author": "John"},
    )
    client.post("/books/1/borrow")

    response = client.get("/books?available=false")

    assert response.status_code == 200
    books = response.get_json()
    assert len(books) == 1
    assert books[0]["available"] is False
