"""Auth Pydantic schemas for request/response validation."""

from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from backend.utils.validators import is_strong_password


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    role: Literal["student", "teacher", "admin"] = "student"

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError(
                "Password must be at least 8 characters and contain uppercase, "
                "lowercase, digit, and special character (@$!%*?&)."
            )
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int  # seconds


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError(
                "Password must be at least 8 characters and contain uppercase, "
                "lowercase, digit, and special character."
            )
        return v


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not is_strong_password(v):
            raise ValueError(
                "Password must contain uppercase, lowercase, digit, and special character."
            )
        return v


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_active: bool
    avatar: Optional[str] = None
    created_at: str
