
# Manual API Testing Report

## Testing Environment
- Framework: Flask
- Python Version: 3.14.3
- Testing Tool: PowerShell Invoke-RestMethod
- Base URL: http://127.0.0.1:5000

## Manual Test Cases

| Test No. | API Request | Expected Status | Result |
|---|---|---:|---|
| 1 | POST /books | 201 Created | PASS |
| 2 | GET /books | 200 OK | PASS |
| 3 | GET /books/1 | 200 OK | PASS |
| 4 | PUT /books/1 | 200 OK | PASS |
| 5 | DELETE /books/1 | 204 No Content | PASS |
| 6 | POST /books | 201 Created | PASS |
| 7 | POST /books/2/borrow | 200 OK | PASS |
| 8 | POST /books/2/return | 200 OK | PASS |

## Test Observations

1. A new book was created successfully.
2. All books were retrieved successfully.
3. A specific book was retrieved using its ID.
4. Book details were updated successfully.
5. A book was deleted successfully.
6. Another book was created successfully.
7. The book availability changed to false after borrowing.
8. The book availability changed to true after returning.

## Conclusion

All eight listed manual API test scenarios were
executed successfully using PowerShell.

The API returned the expected responses for these
scenarios.
