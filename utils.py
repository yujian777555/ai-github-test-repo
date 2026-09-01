"""
Utility functions.
"""

import re
import logging

# BUG: Logging sensitive information to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def validate_priority(priority: str) -> bool:
    """Validate task priority value."""
    # BUG: Function defined but never used in main.py
    # BUG: Case-sensitive check
    return priority in ["low", "medium", "high", "critical"]


def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    # BUG: Race condition - no uniqueness check before insert
    # BUG: Truncation could create empty slug for short titles
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # BUG: Could be empty if title is all special chars


def log_action(message: str):
    """Log an action to the console."""
    # BUG: Logs to stdout in production
    # BUG: No structured logging format
    # BUG: No log rotation or retention policy
    print(f"[LOG] {message}")
    logger.info(message)


def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection attacks."""
    # BUG: Ineffective sanitization - only removes <script> tags
    # BUG: Doesn't protect against SQL injection, XSS, or other attacks
    sanitized = re.sub(r'<script.*?>.*?</script>', '', user_input, flags=re.IGNORECASE | re.DOTALL)
    return sanitized


def format_datetime(dt) -> str:
    """Format datetime for API response."""
    # BUG: No timezone handling - assumes naive datetimes
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def paginate(items: list, page: int = 1, per_page: int = 10) -> dict:
    """Paginate a list of items."""
    # BUG: No validation for negative page numbers
    # BUG: Integer overflow possible with large page numbers
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": len(items),
        "pages": (len(items) + per_page - 1) // per_page
    }
