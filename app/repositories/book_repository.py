

"""SQLite repository for storing library books."""

from app.database import get_connection
from app.models import Book


class BookRepository:
    """Manage book data using SQLite storage."""

    @staticmethod
    def _to_book(row) -> Book | None:
        """Convert a database row into a Book object."""
        if row is None:
            return None

        return Book(
            id=row["id"],
            title=row["title"],
            author=row["author"],
            isbn=row["isbn"],
            year=row["year"],
            available=bool(row["available"]),
        )

    def create(
        self,
        title: str,
        author: str,
        isbn: str | None,
        year: int | None,
    ) -> Book:
        """Create and store a new book."""
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO books (title, author, isbn, year)
                VALUES (?, ?, ?, ?)
                """,
                (title, author, isbn, year),
            )
            book_id = cursor.lastrowid

        return self.get_by_id(book_id)

    def get_by_id(self, book_id: int) -> Book | None:
        """Find a book using its ID."""
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM books WHERE id = ?",
                (book_id,),
            ).fetchone()

        return self._to_book(row)

    def get_all(self) -> list[Book]:
        """Return all stored books."""
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM books ORDER BY id"
            ).fetchall()

        return [self._to_book(row) for row in rows]

    def find_by_isbn(
        self,
        isbn: str,
        exclude_id: int | None = None,
    ) -> Book | None:
        """Find a book using its ISBN."""
        with get_connection() as connection:
            if exclude_id is None:
                row = connection.execute(
                    "SELECT * FROM books WHERE isbn = ?",
                    (isbn,),
                ).fetchone()
            else:
                row = connection.execute(
                    "SELECT * FROM books WHERE isbn = ? AND id != ?",
                    (isbn, exclude_id),
                ).fetchone()

        return self._to_book(row)

    def update(
        self,
        book_id: int,
        title: str,
        author: str,
        isbn: str | None,
        year: int | None,
    ) -> Book | None:
        """Update an existing book."""
        with get_connection() as connection:
            cursor = connection.execute(
                """
                UPDATE books
                SET title = ?, author = ?, isbn = ?, year = ?
                WHERE id = ?
                """,
                (title, author, isbn, year, book_id),
            )

            if cursor.rowcount == 0:
                return None

        return self.get_by_id(book_id)

    def set_availability(
        self,
        book_id: int,
        available: bool,
    ) -> Book | None:
        """Update a book's availability."""
        with get_connection() as connection:
            cursor = connection.execute(
                "UPDATE books SET available = ? WHERE id = ?",
                (int(available), book_id),
            )

            if cursor.rowcount == 0:
                return None

        return self.get_by_id(book_id)

    def delete(self, book_id: int) -> bool:
        """Delete a book using its ID."""
        with get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM books WHERE id = ?",
                (book_id,),
            )

        return cursor.rowcount > 0

    def reset(self) -> None:
        """Clear all books and reset the ID counter."""
        with get_connection() as connection:
            connection.execute("DELETE FROM books")
            connection.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'books'"
            )
