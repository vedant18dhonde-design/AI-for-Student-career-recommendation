"""Auth routes — all authentication endpoints."""

from fastapi import APIRouter, Depends

from backend.core.dependencies import get_current_user
from backend.utils.response import created_response, success_response

from .schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    ResetPasswordRequest,
)
from .service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", summary="Register a new user")
async def register(request: RegisterRequest):
    data = await auth_service.register(request)
    return created_response(data=data, message="Account created successfully.")


@router.post("/login", summary="Login with email and password")
async def login(request: LoginRequest):
    data = await auth_service.login(request)
    return success_response(data=data, message="Logged in successfully.")


@router.post("/logout", summary="Logout and revoke refresh token")
async def logout(request: RefreshTokenRequest):
    data = await auth_service.logout(request.refresh_token)
    return success_response(data=data, message="Logged out successfully.")


@router.post("/refresh", summary="Refresh access token")
async def refresh(request: RefreshTokenRequest):
    data = await auth_service.refresh_access_token(request)
    return success_response(data=data, message="Token refreshed.")


@router.post("/forgot-password", summary="Request password reset email")
async def forgot_password(request: ForgotPasswordRequest):
    data = await auth_service.forgot_password(request)
    return success_response(data=data, message=data["message"])


@router.post("/reset-password", summary="Reset password using token")
async def reset_password(request: ResetPasswordRequest):
    data = await auth_service.reset_password(request)
    return success_response(data=data, message=data["message"])


@router.post("/change-password", summary="Change password for logged-in user")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await auth_service.change_password(current_user, request)
    return success_response(data=data, message=data["message"])


@router.get("/me", summary="Get current user info")
async def me(current_user: dict = Depends(get_current_user)):
    return success_response(data={
        "id": str(current_user["_id"]),
        "name": current_user["name"],
        "email": current_user["email"],
        "role": current_user["role"],
        "is_active": current_user["is_active"],
        "avatar": current_user.get("avatar"),
        "created_at": str(current_user["created_at"]),
    })
