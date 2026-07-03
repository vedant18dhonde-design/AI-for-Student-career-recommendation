"""FastAPI dependency injection providers."""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.core.database import Collections, get_collection
from backend.core.security import decode_token

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
):
    """Extract and validate the current user from the Authorization header."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise credentials_exception

    user_id: Optional[str] = payload.get("sub")
    if not user_id:
        raise credentials_exception

    # Fetch user from DB
    from bson import ObjectId
    users = get_collection(Collections.USERS)
    try:
        user = await users.find_one({"_id": ObjectId(user_id), "is_active": True})
    except Exception:
        raise credentials_exception

    if not user:
        raise credentials_exception

    return user


def require_roles(*roles: str):
    """Role-based access control dependency factory."""
    async def _role_checker(current_user: dict = Depends(get_current_user)):
        if current_user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(roles)}",
            )
        return current_user
    return _role_checker


# Convenience role dependencies
require_student = require_roles("student")
require_teacher = require_roles("teacher", "admin")
require_admin = require_roles("admin")
require_any = require_roles("student", "teacher", "admin")
