from flask import Flask, abort

from app.errors import register_error_handlers


def test_unmapped_http_error_returns_internal_error():
    app = Flask(__name__)
    register_error_handlers(app)

    @app.get("/teapot")
    def teapot():
        abort(418)

    client = app.test_client()
    response = client.get("/teapot")

    assert response.status_code == 418
    assert response.get_json()["error"]["code"] == "INTERNAL_ERROR"
