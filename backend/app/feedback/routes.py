"""Feedback repository, service, and routes."""

import logging
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from bson import ObjectId
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field

from backend.core.database import Collections, get_collection
from backend.core.dependencies import get_current_user, require_admin
from backend.utils.pagination import PaginationParams
from backend.utils.response import created_response, paginated_response, success_response

logger = logging.getLogger(__name__)


# ── Schemas ───────────────────────────────────────────────────────────────────

class CreateFeedbackRequest(BaseModel):
    subject: str = Field(..., min_length=5)
    message: str = Field(..., min_length=10)
    category: str = Field(default="general", description="general/bug/feature/complaint/praise")
    rating: Optional[int] = Field(None, ge=1, le=5)


class FeedbackReplyRequest(BaseModel):
    reply: str = Field(..., min_length=5)


# ── Repository ────────────────────────────────────────────────────────────────

class FeedbackRepository:
    @property
    def feedback(self):
        return get_collection(Collections.FEEDBACK)

    async def create(self, user_id: str, user_name: str, data: dict) -> dict:
        doc = {
            "user_id": user_id,
            "user_name": user_name,
            "subject": data["subject"],
            "message": data["message"],
            "category": data.get("category", "general"),
            "rating": data.get("rating"),
            "status": "open",
            "reply": None,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
        }
        result = await self.feedback.insert_one(doc)
        doc["_id"] = result.inserted_id
        return doc

    async def list_all(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
    ) -> Tuple[List[dict], int]:
        query = {}
        if status:
            query["status"] = status
        if category:
            query["category"] = category
        total = await self.feedback.count_documents(query)
        cursor = self.feedback.find(query).sort("created_at", -1).skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        return docs, total

    async def list_by_user(self, user_id: str) -> List[dict]:
        cursor = self.feedback.find({"user_id": user_id}).sort("created_at", -1)
        return await cursor.to_list(length=50)

    async def reply(self, feedback_id: str, reply_text: str) -> bool:
        result = await self.feedback.update_one(
            {"_id": ObjectId(feedback_id)},
            {"$set": {"reply": reply_text, "status": "resolved", "updated_at": datetime.now(timezone.utc)}},
        )
        return result.modified_count > 0


feedback_repository = FeedbackRepository()


def _serialize(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "user_name": doc.get("user_name", ""),
        "subject": doc["subject"],
        "message": doc["message"],
        "category": doc["category"],
        "rating": doc.get("rating"),
        "status": doc["status"],
        "reply": doc.get("reply"),
        "created_at": str(doc["created_at"]),
    }


# ── Router ────────────────────────────────────────────────────────────────────

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", summary="Submit feedback")
async def submit_feedback(
    request: CreateFeedbackRequest,
    current_user: dict = Depends(get_current_user),
):
    doc = await feedback_repository.create(str(current_user["_id"]), current_user["name"], request.model_dump())
    return created_response(data=_serialize(doc), message="Feedback submitted. Thank you!")


@router.get("/my", summary="Get my feedback")
async def my_feedback(current_user: dict = Depends(get_current_user)):
    docs = await feedback_repository.list_by_user(str(current_user["_id"]))
    return success_response(data=[_serialize(d) for d in docs])


@router.get("/", summary="List all feedback (admin)")
async def list_feedback(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(require_admin),
):
    docs, total = await feedback_repository.list_all(status, category, pagination.skip, pagination.limit)
    return paginated_response([_serialize(d) for d in docs], total, pagination.page, pagination.page_size)


@router.post("/{feedback_id}/reply", summary="Reply to feedback (admin)")
async def reply_feedback(
    feedback_id: str,
    request: FeedbackReplyRequest,
    current_user: dict = Depends(require_admin),
):
    await feedback_repository.reply(feedback_id, request.reply)
    return success_response(message="Reply sent.")
