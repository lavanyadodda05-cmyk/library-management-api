
# Library Management API Documentation

## Base URL

http://127.0.0.1:5000

## 1. Health Check

- Method: GET
- URL: /health
- Purpose: Check whether the API is running.
- Success Status: 200 OK

Response:
```json
{
  "status": "ok"
}
```

## 2. Create a Book

- Method: POST
- URL: /books
- Purpose: Add a new book.
- Success Status: 201 Created

Request Body:
```json
{
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025
}
```

Possible Errors:
- 400 VALIDATION_ERROR: Invalid book details.
- 409 CONFLICT: Duplicate ISBN.

## 3. Get All Books

- Method: GET
- URL: /books
- Purpose: Retrieve all books.
- Optional Query Parameters:
  - author: Filter by author.
  - available: Filter by true or false.
- Success Status: 200 OK

Possible Errors:
- 400 VALIDATION_ERROR: Invalid available filter.

## 4. Get a Book by ID

- Method: GET
- URL: /books/{book_id}
- Purpose: Retrieve one book using its ID.
- Success Status: 200 OK

Possible Errors:
- 404 NOT_FOUND: Book does not exist.

## 5. Update a Book

- Method: PUT
- URL: /books/{book_id}
- Purpose: Update title, author, ISBN, and year.
- Success Status: 200 OK

Request Body:
```json
{
  "title": "Advanced Python",
  "author": "John",
  "isbn": "1234567890",
  "year": 2026
}
```

Possible Errors:
- 400 VALIDATION_ERROR: Invalid book details.
- 404 NOT_FOUND: Book does not exist.
- 409 CONFLICT: Duplicate ISBN.

## 6. Delete a Book

- Method: DELETE
- URL: /books/{book_id}
- Purpose: Remove a book.
- Success Status: 204 No Content

Possible Errors:
- 404 NOT_FOUND: Book does not exist.

## 7. Borrow a Book

- Method: POST
- URL: /books/{book_id}/borrow
- Purpose: Borrow an available book.
- Success Status: 200 OK

Expected Behavior:
The available field changes from true to false.

Possible Errors:
- 404 NOT_FOUND: Book does not exist.
- 409 CONFLICT: Book is already borrowed.

## 8. Return a Book

- Method: POST
- URL: /books/{book_id}/return
- Purpose: Return a borrowed book.
- Success Status: 200 OK

Expected Behavior:
The available field changes from false to true.

Possible Errors:
- 404 NOT_FOUND: Book does not exist.
- 409 CONFLICT: Book has not been borrowed.

## Common Error Response

All API errors use this JSON structure:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Book 42 not found."
  }
}
```

## Storage

The application uses in-memory Python storage.
No database is used. All book data is lost when
the application restarts.
