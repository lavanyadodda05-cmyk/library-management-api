
"""Main application entry point."""

import logging

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.database import init_db
from app.errors import register_error_handlers
from app.routes.books import books_bp
from app.routes.health import health_bp


def create_app() -> Flask:
    """Create and configure the Flask application."""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "http://127.0.0.1:3000",
                ]
            }
        },
    )

    init_db()

    app.register_blueprint(health_bp)
    app.register_blueprint(books_bp)

    register_error_handlers(app)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=False,
    )
