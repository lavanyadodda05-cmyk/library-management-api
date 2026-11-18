"""Database connection and initialization."""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent.parent
    / "instance"
    / "library.db"
)


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Create and manage a SQLite database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db() -> None:
    """Create the books table if it does not exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                year INTEGER,
                available INTEGER NOT NULL DEFAULT 1
            )
            """
        )