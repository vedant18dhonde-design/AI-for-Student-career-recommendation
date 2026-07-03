"""Users repository — MongoDB operations for user profiles."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from bson import ObjectId

from backend.core.database import Collections, get_collection

logger = logging.getLogger(__name__)


class UsersRepository:
    @property
    def users(self):
        return get_collection(Collections.USERS)

    async def find_by_id(self, user_id: str) -> Optional[dict]:
        try:
            return await self.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    async def update_profile(self, user_id: str, update_data: dict) -> Optional[dict]:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
        )
        return await self.find_by_id(user_id)

    async def list_users(
        self,
        role: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> tuple[List[dict], int]:
        query: dict = {"is_active": True}
        if role:
            query["role"] = role
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
            ]

        total = await self.users.count_documents(query)
        cursor = self.users.find(query, {"password_hash": 0}).sort(sort_by, sort_order).skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return users, total

    async def deactivate_user(self, user_id: str) -> None:
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": False, "updated_at": datetime.now(timezone.utc)}},
        )

    async def activate_user(self, user_id: str) -> None:
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_active": True, "updated_at": datetime.now(timezone.utc)}},
        )

    async def count_by_role(self, role: str) -> int:
        return await self.users.count_documents({"role": role, "is_active": True})

    async def get_stats(self) -> dict:
        total = await self.users.count_documents({})
        students = await self.count_by_role("student")
        teachers = await self.count_by_role("teacher")
        admins = await self.count_by_role("admin")
        active = await self.users.count_documents({"is_active": True})
        return {
            "total_users": total,
            "students": students,
            "teachers": teachers,
            "admins": admins,
            "active_users": active,
        }


users_repository = UsersRepository()
