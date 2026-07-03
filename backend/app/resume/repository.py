"""Resume repository."""

import logging
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from backend.core.database import Collections, get_collection

logger = logging.getLogger(__name__)


class ResumeRepository:
    @property
    def resumes(self):
        return get_collection(Collections.RESUMES)

    async def create_or_update(self, user_id: str, data: dict) -> dict:
        data["user_id"] = user_id
        data["updated_at"] = datetime.now(timezone.utc)
        result = await self.resumes.find_one_and_update(
            {"user_id": user_id},
            {"$set": data, "$setOnInsert": {"created_at": datetime.now(timezone.utc)}},
            upsert=True,
            return_document=True,
        )
        return result if result else await self.resumes.find_one({"user_id": user_id})

    async def find_by_user(self, user_id: str) -> Optional[dict]:
        return await self.resumes.find_one({"user_id": user_id})


resume_repository = ResumeRepository()
