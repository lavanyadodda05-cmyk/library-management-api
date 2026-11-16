
# Library Management API

A RESTful Library Management API built using Python and Flask. It supports creating, retrieving, updating, deleting, borrowing, and returning books.

## Prerequisites

- Python 3.10 or above
- pip
- Flask
- pytest
- pytest-cov

## Setup

1. Clone or download the project.
2. Open the project folder in VS Code.
3. Create a virtual environment:

   ```bash
   py -m venv .venv
   ```

4. Activate the virtual environment on Windows:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Configuration

The application supports these environment variables:

| Variable | Default Value | Description |
|---|---|---|
| APP_HOST | 127.0.0.1 | Application host |
| APP_PORT | 5000 | Application port |
| LOG_LEVEL | INFO | Logging level |

## Run the Application

```bash
python -m app.main
```

The API runs at:

http://127.0.0.1:5000

Health check:

http://127.0.0.1:5000/health

## Run Tests and Reports

Run all tests:

```bash
python -m pytest -v
```

Run tests with coverage:

```bash
python -m pytest --cov=app --cov-report=term-missing
```

Generate JUnit report:

```bash
python -m pytest -v --junitxml=docs/test_results/junit_report.xml
```

## API Summary

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | /health | Health check | 200 |
| POST | /books | Create a book | 201 |
| GET | /books | List books | 200 |
| GET | /books/{book_id} | Get a book | 200 |
| PUT | /books/{book_id} | Update a book | 200 |
| DELETE | /books/{book_id} | Delete a book | 204 |
| POST | /books/{book_id}/borrow | Borrow a book | 200 |
| POST | /books/{book_id}/return | Return a book | 200 |

### Validation and Error Status Codes

- 400: Validation error
- 404: Resource not found
- 405: Method not allowed
- 409: Conflict
- 500: Internal server error

## Project Structure

```text
app/
  routes/
  services/
  repositories/
tests/
docs/
  test_results/
  screenshots/
README.md
requirements.txt
.gitignore
```

## Design Decisions and Assumptions

- Flask is used to build the REST API.
- The application follows a layered architecture:
  - Routes handle HTTP requests and responses.
  - Services handle business logic and validation.
  - Repositories manage book storage.
- Books are stored in Python in-memory storage.
- No database is used.
- Book IDs are generated automatically.
- New books are available by default.
- Book data is lost when the application restarts.
- Pytest is used for automated testing.



