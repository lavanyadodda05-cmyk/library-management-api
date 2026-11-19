
"""Business logic for library book operations."""

from datetime import date

from app.errors import APIError
from app.models import Book
from app.repositories.book_repository import BookRepository


class BookService:
    """Apply validation and business rules to book operations."""

    def __init__(self, repository: BookRepository) -> None:
        """Initialize the book service."""
        self.repository = repository

    def _validate_fields(
        self,
        title: object,
        author: object,
        isbn: object,
        year: object,
    ) -> tuple[str, str, str | None, int | None]:
        """Validate and normalize book fields."""

        if not isinstance(title, str) or not title.strip():
            raise APIError("VALIDATION_ERROR", "Title is required.", 400)

        if len(title.strip()) > 200:
            raise APIError("VALIDATION_ERROR", "Title must not exceed 200 characters.", 400)

        if not isinstance(author, str) or not author.strip():
            raise APIError("VALIDATION_ERROR", "Author is required.", 400)

        if len(author.strip()) > 100:
            raise APIError("VALIDATION_ERROR", "Author must not exceed 100 characters.", 400)

        clean_isbn: str | None = None
        if isbn is not None and isbn != "":
            if not isinstance(isbn, str) or not isbn.isdigit():
                raise APIError("VALIDATION_ERROR", "ISBN must contain only digits.", 400)
            if len(isbn) not in (10, 13):
                raise APIError("VALIDATION_ERROR", "ISBN must contain 10 or 13 digits.", 400)
            clean_isbn = isbn

        clean_year: int | None = None
        if year is not None:
            if isinstance(year, bool) or not isinstance(year, int):
                raise APIError("VALIDATION_ERROR", "Year must be an integer.", 400)
            if not 1000 <= year <= date.today().year:
                raise APIError("VALIDATION_ERROR", "Year is outside the allowed range.", 400)
            clean_year = year

        return title.strip(), author.strip(), clean_isbn, clean_year

    def create_book(
        self,
        title: object,
        author: object,
        isbn: object = None,
        year: object = None,
    ) -> Book:
        """Validate and create a new book."""
        clean_title, clean_author, clean_isbn, clean_year = (
            self._validate_fields(title, author, isbn, year)
        )

        if clean_isbn and self.repository.find_by_isbn(clean_isbn):
            raise APIError("CONFLICT", "A book with this ISBN already exists.", 409)

        return self.repository.create(
            clean_title, clean_author, clean_isbn, clean_year
        )

    def list_books(
        self,
        author: str | None = None,
        available: bool | None = None,
    ) -> list[Book]:
        """Return books matching the supplied filters."""
        books = self.repository.get_all()

        if author is not None:
            books = [
                book for book in books
                if book.author.casefold() == author.casefold()
            ]

        if available is not None:
            books = [
                book for book in books
                if book.available is available
            ]

        return books

    def get_book(self, book_id: int) -> Book:
        """Return a book by ID or raise an error."""
        book = self.repository.get_by_id(book_id)

        if book is None:
            raise APIError("NOT_FOUND", f"Book {book_id} not found.", 404)

        return book

    def update_book(
        self,
        book_id: int,
        title: object,
        author: object,
        isbn: object = None,
        year: object = None,
    ) -> Book:
        """Validate and update an existing book."""
        self.get_book(book_id)

        clean_title, clean_author, clean_isbn, clean_year = (
            self._validate_fields(title, author, isbn, year)
        )

        if clean_isbn and self.repository.find_by_isbn(clean_isbn, book_id):
            raise APIError("CONFLICT", "A book with this ISBN already exists.", 409)

        updated_book = self.repository.update(
            book_id, clean_title, clean_author, clean_isbn, clean_year
        )

        if updated_book is None:
            raise APIError("NOT_FOUND", f"Book {book_id} not found.", 404)

        return updated_book

    def delete_book(self, book_id: int) -> None:
        """Delete a book or raise an error if it does not exist."""
        if not self.repository.delete(book_id):
            raise APIError("NOT_FOUND", f"Book {book_id} not found.", 404)

    def borrow_book(self, book_id: int) -> Book:
        """Mark an available book as borrowed."""
        book = self.get_book(book_id)

        if not book.available:
            raise APIError("CONFLICT", "This book is already borrowed.", 409)

        updated_book = self.repository.update_availability(book_id, False)

        if updated_book is None:
            raise APIError("NOT_FOUND", f"Book {book_id} not found.", 404)

        return updated_book

    def return_book(self, book_id: int) -> Book:
        """Mark a borrowed book as available."""
        book = self.get_book(book_id)

        if book.available:
            raise APIError("CONFLICT", "This book has not been borrowed.", 409)

        updated_book = self.repository.update_availability(book_id, True)

        if updated_book is None:
            raise APIError("NOT_FOUND", f"Book {book_id} not found.", 404)

        return updated_book    


book_repository = BookRepository()
book_service = BookService(book_repository)
