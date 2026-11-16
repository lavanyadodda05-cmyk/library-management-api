
"""Tests for the health check endpoint."""

from flask.testing import FlaskClient


def test_health_check(client: FlaskClient) -> None:
    """Check that the health endpoint returns a successful response."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
