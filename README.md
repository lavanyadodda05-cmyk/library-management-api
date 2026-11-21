
# Library Management API

A RESTful Library Management API built using Python and Flask. It supports creating, retrieving, updating, deleting, borrowing, and returning books.

## Prerequisites

- Python 3.10 or above
- pip
- Flask 3.x
- pytest
- pytest-cov

## Setup

1. Clone or download the project.
2. Open the project folder in VS Code.
3. Create a virtual environment:

```powershell
py -m venv .venv
```

4. Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

5. Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

6. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configuration

The application supports the following environment variables:

| Variable | Default Value | Description |
|---|---|---|
| APP_HOST | 127.0.0.1 | Application host |
| APP_PORT | 5000 | Application port |
| LOG_LEVEL | INFO | Logging level |

## Run the Application

Start the Flask application:

```powershell
python -m app.main
```

The API runs at:

`http://127.0.0.1:5000`

Health check endpoint:

`http://127.0.0.1:5000/health`

Expected health check response:

```json
{
  "status": "ok"
}
```

## Run Tests and Reports

Run all automated tests:

```powershell
python -m pytest -v
```

Run tests with coverage:

```powershell
python -m pytest --cov=app --cov-report=term-missing
```

Generate JUnit XML and save pytest output:

```powershell
python -m pytest -v --junitxml=docs/test_results/junit_report.xml | Tee-Object -FilePath docs/test_results/pytest_output.txt
```

Generate and save coverage report:

```powershell
python -m pytest --cov=app --cov-report=term-missing | Tee-Object -FilePath docs/test_results/coverage_report.txt
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

### Validation Rules

- Title is required and must contain 1–200 characters.
- Author is required and must contain 1–100 characters.
- ISBN is optional and must contain exactly 10 or 13 digits.
- ISBN must be unique.
- Year is optional and must be between 1000 and the current year.
- Book ID is generated automatically.
- New books are available by default.

### Validation and Error Status Codes

| Status Code | Error Code | Description |
|---|---|---|
| 400 | VALIDATION_ERROR | Invalid or missing input |
| 404 | NOT_FOUND | Resource not found |
| 405 | METHOD_NOT_ALLOWED | HTTP method not allowed |
| 409 | CONFLICT | Duplicate ISBN or invalid borrow/return operation |
| 500 | INTERNAL_ERROR | Unexpected server error |

All errors are returned in a consistent JSON format.

## Project Structure

```text
library_management_api/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|   |-- config.py
|   |-- models.py
|   |-- errors.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- health.py
|   |   |-- books.py
|   |-- services/
|   |   |-- __init__.py
|   |   |-- book_service.py
|   |-- repositories/
|       |-- __init__.py
|       |-- book_repository.py
|
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_health.py
|   |-- test_books_crud.py
|   |-- test_books_validation.py
|   |-- test_books_borrow_return.py
|
|-- docs/
|   |-- api_documentation.md
|   |-- test_results/
|   |-- screenshots/
|
|-- .gitignore
|-- README.md
|-- requirements.txt
```

## Design Decisions and Assumptions

- Flask is used to build the REST API.
- The application follows a layered architecture:
  - Routes handle HTTP requests and responses.
  - Services handle business logic and validation.
  - Repositories manage database operations.
- SQLite is used for persistent book storage.
- The database is initialized automatically by the application.
- Book data persists across application restarts as long as the database file is retained.
- Book IDs are generated automatically by the server.
- New books are available by default.
- Only borrow and return operations change book availability.
- Centralized error handling provides consistent JSON error responses.
- Pytest is used for automated testing.
- pytest-cov is used to measure code coverage.

## Documentation and Test Evidence

- API endpoint details: `docs/api_documentation.md`
- Manual API testing results: `docs/test_results/manual_api_tests.md`
- Pytest output: `docs/test_results/pytest_output.txt`
- JUnit report: `docs/test_results/junit_report.xml`
- Coverage report: `docs/test_results/coverage_report.txt`
- Git history: `docs/test_results/git_log.txt`
- Application and testing screenshots: `docs/screenshots/`
