
"""Health check endpoint for the library API."""

from flask import Blueprint, Response, jsonify


health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check() -> tuple[Response, int]:
    """Return the application health status."""
    return jsonify({"status": "ok"}), 200

