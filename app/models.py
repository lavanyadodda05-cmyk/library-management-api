
"""Book model for the library application."""

from dataclasses import dataclass


@dataclass
class Book:
    """Represent a book in the library."""

    id: int
    title: str
    author: str
    isbn: str | None = None
    year: int | None = None
    available: bool = True
