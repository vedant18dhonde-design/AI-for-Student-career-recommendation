"""Notifications repository and service combined."""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from bson import ObjectId

from backend.core.database import Collections, get_collection

logger = logging.getLogger(__name__)


class NotificationsRepository:
    @property
    def notifications(self):
        return get_collection(Collections.NOTIFICATIONS)

    async def create(self, user_id: str, title: str, message: str, notification_type: str = "info") -> dict:
        doc = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "is_read": False,
            "created_at": datetime.now(timezone.utc),
        }
        result = await self.notifications.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def get_user_notifications(
        self, user_id: str, skip: int = 0, limit: int = 20, unread_only: bool = False
    ) -> Tuple[List[dict], int]:
        query = {"user_id": user_id}
        if unread_only:
            query["is_read"] = False
        total = await self.notifications.count_documents(query)
        cursor = self.notifications.find(query).sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return docs, total

    async def mark_read(self, notification_id: str, user_id: str) -> bool:
        result = await self.notifications.update_one(
            {"_id": ObjectId(notification_id), "user_id": user_id},
            {"$set": {"is_read": True}},
        )
        return result.modified_count > 0

    async def mark_all_read(self, user_id: str) -> int:
        result = await self.notifications.update_many(
            {"user_id": user_id, "is_read": False},
            {"$set": {"is_read": True}},
        )
        return result.modified_count

    async def unread_count(self, user_id: str) -> int:
        return await self.notifications.count_documents({"user_id": user_id, "is_read": False})

    async def broadcast(self, title: str, message: str, role: Optional[str] = None) -> int:
        from backend.core.database import get_collection, Collections
        users_col = get_collection(Collections.USERS)
        query = {"is_active": True}
        if role:
            query["role"] = role
        users = await users_col.find(query, {"_id": 1}).to_list(length=10000)
        docs = [
            {
                "user_id": str(u["_id"]),
                "title": title,
                "message": message,
                "type": "announcement",
                "is_read": False,
                "created_at": datetime.now(timezone.utc),
            }
            for u in users
        ]
        if docs:
            await self.notifications.insert_many(docs)
        return len(docs)


def _serialize_notification(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "title": doc["title"],
        "message": doc["message"],
        "type": doc["type"],
        "is_read": doc["is_read"],
        "created_at": str(doc["created_at"]),
    }


notifications_repository = NotificationsRepository()


async def notify_user(user_id: str, title: str, message: str, ntype: str = "info"):
    """Helper to create a notification for a user."""
    try:
        await notifications_repository.create(user_id, title, message, ntype)
    except Exception as exc:
        logger.warning("Failed to create notification for %s: %s", user_id, exc)
