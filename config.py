"""
Configuration module.
Intentionally contains hardcoded secrets and bad practices.
"""

import os

# VULNERABILITY: Hardcoded configuration values
DEBUG = True  # BUG: Debug mode enabled in production
DATABASE_URL = "sqlite:///tasks.db"
API_VERSION = "1.0.0"

# VULNERABILITY: Hardcoded API keys and secrets
JWT_SECRET = "my-super-secret-key-12345"
API_KEY = "sk-live-51234567890abcdef"

# VULNERABILITY: Database credentials in plaintext
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "admin"
DB_PASSWORD = "admin123"  # BUG: Hardcoded password
DB_NAME = "taskmanager"

# BUG: No environment-based configuration
# The correct way would be:
# DEBUG = os.getenv("DEBUG", "False").lower() == "true"
# JWT_SECRET = os.getenv("JWT_SECRET")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
