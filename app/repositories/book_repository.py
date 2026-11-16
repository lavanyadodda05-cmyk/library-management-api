
"""In-memory repository for storing library books."""

from app.models import Book


class BookRepository:
    """Manage book data using in-memory storage."""

    def __init__(self) -> None:
        """Initialize the book storage."""
        self._books: dict[int, Book] = {}
        self._next_id: int = 1

    def create(
        self,
        title: str,
        author: str,
        isbn: str | None,
        year: int | None,
    ) -> Book:
        """Create and store a new book."""
        book = Book(
            id=self._next_id,
            title=title,
            author=author,
            isbn=isbn,
            year=year,
            available=True,
        )
        self._books[book.id] = book
        self._next_id += 1
        return book

    def get_by_id(self, book_id: int) -> Book | None:
        """Find a book using its ID."""
        return self._books.get(book_id)

    def get_all(self) -> list[Book]:
        """Return all stored books."""
        return list(self._books.values())

    def find_by_isbn(
        self,
        isbn: str,
        exclude_id: int | None = None,
    ) -> Book | None:
        """Find a book using its ISBN."""
        for book in self._books.values():
            if book.isbn == isbn and book.id != exclude_id:
                return book
        return None

    def update(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str | None,
        year: int | None,
    ) -> Book | None:
        """Update an existing book."""
        book = self.get_by_id(book_id)

        if book is None:
            return None

        book.title = title
        book.author = author
        book.isbn = isbn
        book.year = year

        return book

    def delete(self, book_id: int) -> bool:
        """Delete a book using its ID."""
        if book_id not in self._books:
            return False

        del self._books[book_id]
        return True

    def reset(self) -> None:
        """Clear all books and reset the ID counter."""
        self._books.clear()
        self._next_id = 1
