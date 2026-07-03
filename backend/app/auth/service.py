"""Auth service — business logic for authentication."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status

from backend.config.settings import settings
from backend.core.security import (
    create_access_token,
    create_refresh_token,
    create_reset_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.utils.email import send_password_reset_email, send_welcome_email

from .repository import auth_repository
from .schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
)

logger = logging.getLogger(__name__)


def _serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "is_active": user["is_active"],
        "avatar": user.get("avatar"),
        "created_at": str(user["created_at"]),
    }


def _make_tokens(user_id: str, role: str) -> dict:
    access_token = create_access_token({"sub": user_id, "role": role})
    refresh_token = create_refresh_token({"sub": user_id, "role": role})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


class AuthService:
    async def register(self, request: RegisterRequest) -> dict:
        # Check duplicate email
        existing = await auth_repository.find_by_email(request.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="An account with this email already exists.",
            )

        hashed = hash_password(request.password)
        user = await auth_repository.create_user({
            "name": request.name.strip(),
            "email": request.email.lower(),
            "password_hash": hashed,
            "role": request.role,
            "profile": {},
            "avatar": None,
        })

        # Send welcome email (non-blocking)
        await send_welcome_email(request.email, request.name)

        user_id = str(user["_id"])
        tokens = _make_tokens(user_id, request.role)

        # Store refresh token
        await auth_repository.store_refresh_token(
            user_id=user_id,
            token=tokens["refresh_token"],
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return {"user": _serialize_user(user), **tokens}

    async def login(self, request: LoginRequest) -> dict:
        user = await auth_repository.find_by_email(request.email)
        if not user or not verify_password(request.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
            )
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been deactivated. Contact support.",
            )

        user_id = str(user["_id"])
        tokens = _make_tokens(user_id, user["role"])

        await auth_repository.store_refresh_token(
            user_id=user_id,
            token=tokens["refresh_token"],
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        )

        return {"user": _serialize_user(user), **tokens}

    async def logout(self, refresh_token: str) -> dict:
        await auth_repository.revoke_refresh_token(refresh_token)
        return {"message": "Logged out successfully"}

    async def refresh_access_token(self, request: RefreshTokenRequest) -> dict:
        payload = decode_token(request.refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        stored = await auth_repository.find_refresh_token(request.refresh_token)
        if not stored:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked.",
            )

        user_id = payload.get("sub")
        user = await auth_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        # Rotate refresh token
        await auth_repository.revoke_refresh_token(request.refresh_token)
        tokens = _make_tokens(user_id, user["role"])
        await auth_repository.store_refresh_token(
            user_id=user_id,
            token=tokens["refresh_token"],
            expires_at=datetime.now(timezone.utc) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        )
        return tokens

    async def forgot_password(self, request: ForgotPasswordRequest) -> dict:
        user = await auth_repository.find_by_email(request.email)
        # Always return success to prevent email enumeration
        if user:
            token = create_reset_token()
            expires_at = datetime.now(timezone.utc) + timedelta(
                minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
            )
            await auth_repository.store_reset_token(request.email, token, expires_at)
            await send_password_reset_email(request.email, token)
        return {"message": "If that email exists, a reset link has been sent."}

    async def reset_password(self, request: ResetPasswordRequest) -> dict:
        stored = await auth_repository.find_reset_token(request.token)
        if not stored:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token.",
            )
        if stored["expires_at"] < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reset token has expired.",
            )

        hashed = hash_password(request.new_password)
        await auth_repository.update_user_by_email(stored["email"], {"password_hash": hashed})
        await auth_repository.delete_reset_token(request.token)
        return {"message": "Password reset successfully."}

    async def change_password(self, user: dict, request: ChangePasswordRequest) -> dict:
        if not verify_password(request.current_password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect.",
            )
        hashed = hash_password(request.new_password)
        await auth_repository.update_user(str(user["_id"]), {"password_hash": hashed})
        await auth_repository.revoke_all_user_tokens(str(user["_id"]))
        return {"message": "Password changed successfully. Please log in again."}


auth_service = AuthService()
