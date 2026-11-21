# Library Management API Documentation

## Base URL

`http://127.0.0.1:5000`

All request and response bodies use JSON unless otherwise specified.

## 1. Health Check

- **Method:** GET
- **URL:** `/health`
- **Purpose:** Check whether the API is running.
- **Success Status:** `200 OK`

**Example Response:**

```json
{
  "status": "ok"
}
```

## 2. Create a Book

- **Method:** POST
- **URL:** `/books`
- **Purpose:** Add a new book to the library.
- **Success Status:** `201 Created`

**Example Request Body:**

```json
{
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025
}
```

**Example Success Response:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025,
  "available": true
}
```

**Validation Rules:**
- `title` is required and must contain 1–200 characters after trimming.
- `author` is required and must contain 1–100 characters after trimming.
- `isbn` is optional and must contain exactly 10 or 13 digits when provided.
- `year` is optional and must be an integer between 1000 and the current year.
- `id` is generated automatically by the server.
- `available` is automatically set to `true` when a book is created.

**Possible Errors:**
- `400 VALIDATION_ERROR`: Missing or invalid book details.
- `409 CONFLICT`: ISBN already exists.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 3. Get All Books

- **Method:** GET
- **URL:** `/books`
- **Purpose:** Retrieve all books from the library.
- **Success Status:** `200 OK`

**Optional Query Parameters:**

| Parameter | Description | Example |
|---|---|---|
| `author` | Filter by exact author name, case-insensitive | `?author=John` |
| `available` | Filter by availability | `?available=true` |

**Example Request:**

`GET /books?available=true`

**Example Success Response:**

```json
[
  {
    "id": 1,
    "title": "Python Basics",
    "author": "John",
    "isbn": "1234567890",
    "year": 2025,
    "available": true
  }
]
```

If no books are available, the API returns an empty array:

```json
[]
```

**Possible Errors:**
- `400 VALIDATION_ERROR`: Invalid `available` query parameter.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 4. Get a Book by ID

- **Method:** GET
- **URL:** `/books/{book_id}`
- **Purpose:** Retrieve one book using its unique ID.
- **Success Status:** `200 OK`

**Example Request:**

`GET /books/1`

**Example Success Response:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025,
  "available": true
}
```

**Possible Errors:**
- `404 NOT_FOUND`: Book does not exist.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 5. Update a Book

- **Method:** PUT
- **URL:** `/books/{book_id}`
- **Purpose:** Update the title, author, ISBN, and year of an existing book.
- **Success Status:** `200 OK`

**Example Request:**

`PUT /books/1`

**Request Body:**

```json
{
  "title": "Advanced Python",
  "author": "John",
  "isbn": "1234567890",
  "year": 2026
}
```

**Example Success Response:**

```json
{
  "id": 1,
  "title": "Advanced Python",
  "author": "John",
  "isbn": "1234567890",
  "year": 2026,
  "available": true
}
```

**Important Rules:**
- All required book details must be provided.
- The book ID cannot be changed.
- The availability status cannot be changed through this endpoint.
- ISBN must remain unique.

**Possible Errors:**
- `400 VALIDATION_ERROR`: Missing or invalid book details.
- `404 NOT_FOUND`: Book does not exist.
- `409 CONFLICT`: ISBN already belongs to another book.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 6. Delete a Book

- **Method:** DELETE
- **URL:** `/books/{book_id}`
- **Purpose:** Remove a book from the library.
- **Success Status:** `204 No Content`

**Example Request:**

`DELETE /books/1`

**Example Success Response:**

No response body is returned.

**Possible Errors:**
- `404 NOT_FOUND`: Book does not exist.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 7. Borrow a Book

- **Method:** POST
- **URL:** `/books/{book_id}/borrow`
- **Purpose:** Borrow an available book.
- **Success Status:** `200 OK`

**Example Request:**

`POST /books/1/borrow`

**Example Success Response:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025,
  "available": false
}
```

**Expected Behavior:**

The `available` field changes from `true` to `false`.

**Possible Errors:**
- `404 NOT_FOUND`: Book does not exist.
- `409 CONFLICT`: Book is already borrowed.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## 8. Return a Book

- **Method:** POST
- **URL:** `/books/{book_id}/return`
- **Purpose:** Return a previously borrowed book.
- **Success Status:** `200 OK`

**Example Request:**

`POST /books/1/return`

**Example Success Response:**

```json
{
  "id": 1,
  "title": "Python Basics",
  "author": "John",
  "isbn": "1234567890",
  "year": 2025,
  "available": true
}
```

**Expected Behavior:**

The `available` field changes from `false` to `true`.

**Possible Errors:**
- `404 NOT_FOUND`: Book does not exist.
- `409 CONFLICT`: Book has not been borrowed.
- `405 METHOD_NOT_ALLOWED`: Unsupported HTTP method.
- `500 INTERNAL_ERROR`: Unexpected server error.

## Common Error Response Format

All API errors use the following JSON structure:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Book 42 not found"
  }
}
```

**Supported Error Codes:**

| Error Code | Description |
|---|---|
| `VALIDATION_ERROR` | Invalid or missing input data |
| `NOT_FOUND` | Requested resource does not exist |
| `CONFLICT` | Duplicate ISBN or invalid borrow/return operation |
| `METHOD_NOT_ALLOWED` | HTTP method is not supported |
| `INTERNAL_ERROR` | Unexpected server error |

Validation errors use HTTP `400 Bad Request` in this application.

## Storage

- The application uses SQLite for persistent book storage.
- The database is initialized automatically by the application.
- Book records are stored in the SQLite database.
- Book data persists across application restarts as long as the database file is retained.
- The repository layer manages database operations.
