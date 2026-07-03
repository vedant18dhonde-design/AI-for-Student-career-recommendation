"""Admin routes — user management, system stats, reports."""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.app.predictions.repository import predictions_repository
from backend.app.users.repository import users_repository
from backend.app.users.service import users_service
from backend.core.dependencies import require_admin
from backend.utils.pagination import PaginationParams
from backend.utils.response import paginated_response, success_response

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", summary="Admin dashboard statistics")
async def dashboard(current_user: dict = Depends(require_admin)):
    user_stats = await users_repository.get_stats()
    total_predictions = await predictions_repository.total_predictions_count()
    type_dist = await predictions_repository.get_type_distribution()
    recent = await predictions_repository.recent_predictions(10)

    return success_response(data={
        "users": user_stats,
        "predictions": {
            "total": total_predictions,
            "by_type": type_dist,
        },
        "recent_predictions": [
            {
                "id": str(p["_id"]),
                "user_id": p["user_id"],
                "type": p["prediction_type"],
                "created_at": str(p["created_at"]),
            }
            for p in recent
        ],
        "system": {
            "status": "healthy",
            "version": "1.0.0",
            "uptime": "Active",
        },
    })


@router.get("/users", summary="List all users")
async def list_users(
    role: Optional[str] = Query(None),
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


@router.get("/users/{user_id}", summary="Get user details")
async def get_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.get_user_by_id(user_id)
    return success_response(data=data)


@router.patch("/users/{user_id}/deactivate", summary="Deactivate user")
async def deactivate_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.deactivate_user(user_id)
    return success_response(data=data, message="User deactivated.")


@router.patch("/users/{user_id}/activate", summary="Activate user")
async def activate_user(user_id: str, current_user: dict = Depends(require_admin)):
    data = await users_service.activate_user(user_id)
    return success_response(data=data, message="User activated.")


@router.get("/predictions/stats", summary="Prediction statistics")
async def prediction_stats(current_user: dict = Depends(require_admin)):
    total = await predictions_repository.total_predictions_count()
    by_type = await predictions_repository.get_type_distribution()
    monthly = await predictions_repository.get_monthly_counts()

    return success_response(data={
        "total": total,
        "by_type": by_type,
        "monthly": monthly,
    })


@router.get("/system/stats", summary="System health statistics")
async def system_stats(current_user: dict = Depends(require_admin)):
    user_stats = await users_repository.get_stats()
    total_predictions = await predictions_repository.total_predictions_count()

    return success_response(data={
        "users": user_stats,
        "total_predictions": total_predictions,
        "system": {
            "status": "healthy",
            "version": "1.0.0",
            "database": "connected",
            "ml_models": "loaded",
        },
    })
