"""Auth repository — all MongoDB operations for authentication."""

import logging
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import Collections, get_collection

logger = logging.getLogger(__name__)


class AuthRepository:
    @property
    def users(self):
        return get_collection(Collections.USERS)

    @property
    def refresh_tokens(self):
        return get_collection(Collections.REFRESH_TOKENS)

    @property
    def reset_tokens(self):
        return get_collection(Collections.RESET_TOKENS)

    async def create_user(self, user_data: dict) -> dict:
        user_data["created_at"] = datetime.now(timezone.utc)
        user_data["updated_at"] = datetime.now(timezone.utc)
        user_data["is_active"] = True
        user_data["is_verified"] = False
        result = await self.users.insert_one(user_data)
        user_data["_id"] = result.inserted_id
        return user_data

    async def find_by_email(self, email: str) -> Optional[dict]:
        return await self.users.find_one({"email": email.lower()})

    async def find_by_id(self, user_id: str) -> Optional[dict]:
        try:
            return await self.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None

    async def update_user(self, user_id: str, update_data: dict) -> Optional[dict]:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.users.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
        )
        return await self.find_by_id(user_id)

    async def store_refresh_token(self, user_id: str, token: str, expires_at: datetime) -> None:
        await self.refresh_tokens.insert_one({
            "user_id": user_id,
            "token": token,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc),
        })

    async def find_refresh_token(self, token: str) -> Optional[dict]:
        return await self.refresh_tokens.find_one({"token": token})

    async def revoke_refresh_token(self, token: str) -> None:
        await self.refresh_tokens.delete_one({"token": token})

    async def revoke_all_user_tokens(self, user_id: str) -> None:
        await self.refresh_tokens.delete_many({"user_id": user_id})

    async def store_reset_token(self, email: str, token: str, expires_at: datetime) -> None:
        await self.reset_tokens.delete_many({"email": email})
        await self.reset_tokens.insert_one({
            "email": email.lower(),
            "token": token,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc),
        })

    async def find_reset_token(self, token: str) -> Optional[dict]:
        return await self.reset_tokens.find_one({"token": token})

    async def update_user_by_email(self, email: str, update_data: dict) -> None:
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.users.update_one({"email": email.lower()}, {"$set": update_data})

    async def delete_reset_token(self, token: str) -> None:
        await self.reset_tokens.delete_one({"token": token})


auth_repository = AuthRepository()
