"""
Security & Configuration Module
"""

from typing import List
from functools import lru_cache

# Settings de CORS
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS = ["*"]

# Limits
MAX_FILE_SIZE = 10_000_000  # 10MB
MAX_TEXT_LENGTH = 10_000_000  # 10M characters
MAX_REQUEST_SIZE = 100_000_000  # 100MB

# Timeouts
REQUEST_TIMEOUT = 60
COMPRESSION_TIMEOUT = 120

# Rate Limiting (considerar implementar con redis en producción)
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 3600  # 1 hora

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

@lru_cache()
def get_settings():
    """Obtener settings configurados"""
    return {
        "cors_origins": CORS_ORIGINS,
        "max_file_size": MAX_FILE_SIZE,
        "max_text_length": MAX_TEXT_LENGTH,
        "request_timeout": REQUEST_TIMEOUT,
    }
