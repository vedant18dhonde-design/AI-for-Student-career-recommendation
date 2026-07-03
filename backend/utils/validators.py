"""Common validators."""

import re


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)


def is_strong_password(password: str) -> bool:
    """At least 8 chars, one uppercase, one lowercase, one digit, one special char."""
    return bool(PASSWORD_REGEX.match(password))


def validate_gpa(gpa: float) -> float:
    if not (0.0 <= gpa <= 4.0):
        raise ValueError("GPA must be between 0.0 and 4.0")
    return gpa


def sanitize_string(value: str) -> str:
    """Strip whitespace and limit length."""
    return value.strip()[:500]
