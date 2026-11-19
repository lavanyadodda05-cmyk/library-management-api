
"""Centralized error handling for the library API."""

import logging

from flask import Flask, Response, jsonify
from werkzeug.exceptions import HTTPException


logger = logging.getLogger(__name__)


class APIError(Exception):
    """Represent a controlled API error."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
    ) -> None:
        """Initialize an API error."""
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code


def register_error_handlers(app: Flask) -> None:
    """Register centralized error handlers."""

    @app.errorhandler(APIError)
    def handle_api_error(error: APIError) -> tuple[Response, int]:
        """Return a controlled API error as JSON."""
        response = jsonify({
            "error": {
                "code": error.code,
                "message": error.message,
            }
        })
        return response, error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException) -> tuple[Response, int]:
        """Return an HTTP error as JSON."""
        if error.code == 404:
            code = "NOT_FOUND"
        elif error.code == 405:
            code = "METHOD_NOT_ALLOWED"
        else:
            code = "INTERNAL_ERROR"

        response = jsonify({
            "error": {
                "code": code,
                "message": error.description,
            }
        })
        return response, int(error.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception) -> tuple[Response, int]:
        """Handle unexpected errors without exposing internal details."""
        logger.exception("Unexpected application error: %s", error)

        response = jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred.",
            }
        })
        return response, 500
