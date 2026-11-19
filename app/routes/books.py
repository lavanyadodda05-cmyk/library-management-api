
"""Book management API endpoints."""

from flask import Blueprint, Response, jsonify, request

from app.errors import APIError
from app.models import Book
from app.services.book_service import book_service


books_bp = Blueprint("books", __name__, url_prefix="/books")


def book_to_dict(book: Book) -> dict[str, object]:
    """Convert a Book object into a dictionary."""
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "year": book.year,
        "available": book.available,
    }


def get_json_payload() -> dict[str, object]:
    """Read and validate a JSON request body."""
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        raise APIError(
            "VALIDATION_ERROR",
            "Request body must be a valid JSON object.",
            400,
        )

    return payload


@books_bp.route("", methods=["POST"])
def create_book() -> tuple[Response, int]:
    """Create a new book."""
    data = get_json_payload()

    book = book_service.create_book(
        title=data.get("title"),
        author=data.get("author"),
        isbn=data.get("isbn"),
        year=data.get("year"),
    )

    return jsonify(book_to_dict(book)), 201


@books_bp.route("", methods=["GET"])
def get_books() -> Response:
    """Return all books with optional filters."""
    author = request.args.get("author")
    available_value = request.args.get("available")
    available = None

    if available_value is not None:
        if available_value.lower() not in ("true", "false"):
            raise APIError(
                "VALIDATION_ERROR",
                "Available must be true or false.",
                400,
            )
        available = available_value.lower() == "true"

    books = book_service.list_books(author, available)

    return jsonify([book_to_dict(book) for book in books])


@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id: int) -> Response:
    """Return one book by its ID."""
    book = book_service.get_book(book_id)
    return jsonify(book_to_dict(book))


@books_bp.route("/<int:book_id>", methods=["PUT"])
def update_book(book_id: int) -> Response:
    """Update an existing book."""
    data = get_json_payload()

    book = book_service.update_book(
        book_id=book_id,
        title=data.get("title"),
        author=data.get("author"),
        isbn=data.get("isbn"),
        year=data.get("year"),
    )

    return jsonify(book_to_dict(book))


@books_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id: int) -> tuple[str, int]:
    """Delete a book."""
    book_service.delete_book(book_id)
    return "", 204


@books_bp.route("/<int:book_id>/borrow", methods=["POST"])
def borrow_book(book_id: int) -> Response:
    """Borrow an available book."""
    book = book_service.borrow_book(book_id)
    return jsonify(book_to_dict(book))


@books_bp.route("/<int:book_id>/return", methods=["POST"])
def return_book(book_id: int) -> Response:
    """Return a borrowed book."""
    book = book_service.return_book(book_id)
    return jsonify(book_to_dict(book))
