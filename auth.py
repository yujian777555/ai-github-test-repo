"""
Authentication module.
Intentionally contains security vulnerabilities for testing.
"""

import hashlib
import time
import jwt

# VULNERABILITY #1: Hardcoded secret key
SECRET_KEY = "my-super-secret-key-12345"

# VULNERABILITY #2: Hardcoded user database (no real DB)
USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        # VULNERABILITY #3: Password stored in plaintext
        "password": "admin123",
        "role": "admin"
    },
    "user1": {
        "id": 2,
        "username": "user1",
        "password": "password123",
        "role": "user"
    }
}


def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user by username and password."""
    user = USERS.get(username)
    if user and user["password"] == password:
        return user
    return None


def create_token(user_id: int, role: str) -> str:
    """Create a JWT token for authenticated user."""
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": time.time() + 3600  # 1 hour expiration
    }
    # VULNERABILITY #4: Using deprecated jwt.encode signature
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token: str) -> dict:
    """Decode and verify a JWT token."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def hash_password(password: str) -> str:
    """Hash a password using MD5."""
    # VULNERABILITY #5: Using MD5 for password hashing (cryptographically broken)
    return hashlib.md5(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    # VULNERABILITY #6: Timing attack vulnerable (no constant-time comparison)
    return hash_password(password) == hashed
