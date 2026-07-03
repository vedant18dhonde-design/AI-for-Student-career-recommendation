"""Users routes — profile and user management endpoints."""

from typing import Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile

from backend.core.dependencies import (
    get_current_user,
    require_admin,
    require_teacher,
)
from backend.utils.pagination import PaginationParams
from backend.utils.response import paginated_response, success_response

from .schemas import UpdateProfileRequest
from .service import users_service

router = APIRouter(prefix="/users", tags=["Users & Profiles"])


# ── Student Profile ──────────────────────────────────────────────────────────

@router.get("/profile", summary="Get current user profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    data = await users_service.get_profile(str(current_user["_id"]))
    return success_response(data=data, message="Profile retrieved.")


@router.put("/profile", summary="Update current user profile")
async def update_profile(
    request: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await users_service.update_profile(str(current_user["_id"]), request)
    return success_response(data=data, message="Profile updated.")


@router.post("/profile/avatar", summary="Upload profile picture")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    data = await users_service.upload_avatar(str(current_user["_id"]), file)
    return success_response(data=data, message="Avatar uploaded.")


# ── Teacher / Admin: Students ────────────────────────────────────────────────

@router.get("/students", summary="List all students (teacher/admin)")
async def list_students(
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(require_teacher),
):
    students, total = await users_service.list_students(
        search=pagination.search,
        skip=pagination.skip,
        limit=pagination.limit,
        sort_by=pagination.sort_by,
        sort_order=pagination.sort_order,
    )
    return paginated_response(students, total, pagination.page, pagination.page_size)


@router.get("/students/{student_id}", summary="Get student by ID (teacher/admin)")
async def get_student(
    student_id: str,
    current_user: dict = Depends(require_teacher),
):
    data = await users_service.get_user_by_id(student_id)
    return success_response(data=data)


# ── Admin: All Users ─────────────────────────────────────────────────────────

@router.get("/", summary="List all users (admin)")
async def list_users(
    role: Optional[str] = Query(None, description="Filter by role"),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(require_admin),
):
    users, total = await users_service.list_all_users(
        role=role,
        search=pagination.search,
        skip=pagination.skip,
        limit=pagination.limit,
        sort_by=pagination.sort_by,
        sort_order=pagination.sort_order,
    )
    return paginated_response(users, total, pagination.page, pagination.page_size)


@router.get("/{user_id}", summary="Get user by ID (admin)")
async def get_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.get_user_by_id(user_id)
    return success_response(data=data)


@router.patch("/{user_id}/deactivate", summary="Deactivate user (admin)")
async def deactivate_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.deactivate_user(user_id)
    return success_response(data=data, message="User deactivated.")


@router.patch("/{user_id}/activate", summary="Activate user (admin)")
async def activate_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.activate_user(user_id)
    return success_response(data=data, message="User activated.")


@router.get("/stats/overview", summary="Get user statistics (admin)")
async def get_stats(current_user: dict = Depends(require_admin)):
    data = await users_service.get_stats()
    return success_response(data=data)
