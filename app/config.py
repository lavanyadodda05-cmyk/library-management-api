
"""Application configuration settings."""

import os


class Config:
    """Store application configuration values."""

    HOST = os.getenv("APP_HOST", "127.0.0.1")
    PORT = int(os.getenv("APP_PORT", "5000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
