"""Notifications routes."""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from backend.core.dependencies import get_current_user, require_admin
from backend.utils.pagination import PaginationParams
from backend.utils.response import paginated_response, success_response

from .repository import (
    _serialize_notification,
    notifications_repository,
)

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class BroadcastRequest(BaseModel):
    title: str
    message: str
    role: Optional[str] = None


@router.get("/", summary="Get user notifications")
async def get_notifications(
    unread_only: bool = Query(False),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
):
    docs, total = await notifications_repository.get_user_notifications(
        user_id=str(current_user["_id"]),
        skip=pagination.skip,
        limit=pagination.limit,
        unread_only=unread_only,
    )
    data = [_serialize_notification(d) for d in docs]
    return paginated_response(data, total, pagination.page, pagination.page_size)


@router.get("/unread-count", summary="Get unread notifications count")
async def unread_count(current_user: dict = Depends(get_current_user)):
    count = await notifications_repository.unread_count(str(current_user["_id"]))
    return success_response(data={"count": count})


@router.patch("/{notification_id}/read", summary="Mark notification as read")
async def mark_read(
    notification_id: str,
    current_user: dict = Depends(get_current_user),
):
    await notifications_repository.mark_read(notification_id, str(current_user["_id"]))
    return success_response(message="Notification marked as read.")


@router.patch("/mark-all-read", summary="Mark all notifications as read")
async def mark_all_read(current_user: dict = Depends(get_current_user)):
    count = await notifications_repository.mark_all_read(str(current_user["_id"]))
    return success_response(data={"marked": count}, message="All notifications marked as read.")


@router.post("/broadcast", summary="Broadcast announcement (admin only)")
async def broadcast(
    request: BroadcastRequest,
    current_user: dict = Depends(require_admin),
):
    count = await notifications_repository.broadcast(request.title, request.message, request.role)
    return success_response(data={"sent_to": count}, message="Announcement sent.")
