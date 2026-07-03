"""Users service — business logic for profile management."""

import logging
from typing import Optional

from fastapi import HTTPException, UploadFile, status

from backend.utils.file_upload import save_profile_image

from .repository import users_repository
from .schemas import UpdateProfileRequest

logger = logging.getLogger(__name__)


def _serialize_user(user: dict) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user.get("email", ""),
        "role": user.get("role", "student"),
        "avatar": user.get("avatar"),
        "phone": user.get("phone"),
        "bio": user.get("bio"),
        "location": user.get("location"),
        "linkedin": user.get("linkedin"),
        "github": user.get("github"),
        "portfolio": user.get("portfolio"),
        "education": user.get("education", []),
        "experience": user.get("experience", []),
        "skills": user.get("skills", []),
        "projects": user.get("projects", []),
        "certifications": user.get("certifications", []),
        "interests": user.get("interests", []),
        "created_at": str(user.get("created_at", "")),
        "updated_at": str(user.get("updated_at", "")),
    }


class UsersService:
    async def get_profile(self, user_id: str) -> dict:
        user = await users_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _serialize_user(user)

    async def update_profile(self, user_id: str, request: UpdateProfileRequest) -> dict:
        update_data = request.model_dump(exclude_none=True)

        # Convert nested models to dicts
        for key in ["education", "experience", "projects", "certifications"]:
            if key in update_data and update_data[key] is not None:
                update_data[key] = [
                    item.model_dump() if hasattr(item, "model_dump") else item
                    for item in update_data[key]
                ]

        user = await users_repository.update_profile(user_id, update_data)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _serialize_user(user)

    async def upload_avatar(self, user_id: str, file: UploadFile) -> dict:
        path = await save_profile_image(file)
        user = await users_repository.update_profile(user_id, {"avatar": path})
        return {"avatar": path, "user": _serialize_user(user)}

    async def list_students(
        self,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> tuple:
        users, total = await users_repository.list_users(
            role="student",
            search=search,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return [_serialize_user(u) for u in users], total

    async def list_all_users(
        self,
        role: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> tuple:
        users, total = await users_repository.list_users(
            role=role,
            search=search,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return [_serialize_user(u) for u in users], total

    async def get_user_by_id(self, user_id: str) -> dict:
        user = await users_repository.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return _serialize_user(user)

    async def deactivate_user(self, user_id: str) -> dict:
        await users_repository.deactivate_user(user_id)
        return {"message": "User deactivated."}

    async def activate_user(self, user_id: str) -> dict:
        await users_repository.activate_user(user_id)
        return {"message": "User activated."}

    async def get_stats(self) -> dict:
        return await users_repository.get_stats()


users_service = UsersService()
