"""Predictions routes — all 5 ML prediction endpoints + history management."""

from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import get_current_user, require_any
from backend.utils.pagination import PaginationParams
from backend.utils.response import created_response, paginated_response, success_response

from .schemas import (
    CareerPredictionRequest,
    ClusterPredictionRequest,
    PlacementPredictionRequest,
    SalaryPredictionRequest,
    SuccessPredictionRequest,
)
from .service import predictions_service

router = APIRouter(prefix="/predictions", tags=["ML Predictions"])


@router.post("/career", summary="Predict career recommendation")
async def predict_career(
    request: CareerPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.predict_career(str(current_user["_id"]), request)
    return created_response(data=data, message="Career prediction completed.")


@router.post("/salary", summary="Predict salary")
async def predict_salary(
    request: SalaryPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.predict_salary(str(current_user["_id"]), request)
    return created_response(data=data, message="Salary prediction completed.")


@router.post("/placement", summary="Predict placement likelihood")
async def predict_placement(
    request: PlacementPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.predict_placement(str(current_user["_id"]), request)
    return created_response(data=data, message="Placement prediction completed.")


@router.post("/success", summary="Predict student success")
async def predict_success(
    request: SuccessPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.predict_success(str(current_user["_id"]), request)
    return created_response(data=data, message="Success prediction completed.")


@router.post("/cluster", summary="Predict student cluster/segment")
async def predict_cluster(
    request: ClusterPredictionRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.predict_cluster(str(current_user["_id"]), request)
    return created_response(data=data, message="Cluster analysis completed.")


@router.get("/history", summary="Get prediction history (paginated)")
async def get_history(
    prediction_type: Optional[str] = Query(None, description="Filter by type: career/salary/placement/success/cluster"),
    pagination: PaginationParams = Depends(),
    current_user: dict = Depends(get_current_user),
):
    items, total = await predictions_service.get_history(
        user_id=str(current_user["_id"]),
        prediction_type=prediction_type,
        skip=pagination.skip,
        limit=pagination.limit,
        sort_by=pagination.sort_by,
        sort_order=pagination.sort_order,
    )
    return paginated_response(items, total, pagination.page, pagination.page_size)


@router.get("/{prediction_id}", summary="Get a specific prediction")
async def get_prediction(
    prediction_id: str,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.get_prediction(prediction_id, str(current_user["_id"]))
    return success_response(data=data)


@router.delete("/{prediction_id}", summary="Delete a prediction")
async def delete_prediction(
    prediction_id: str,
    current_user: dict = Depends(get_current_user),
):
    data = await predictions_service.delete_prediction(prediction_id, str(current_user["_id"]))
    return success_response(data=data, message="Prediction deleted.")
