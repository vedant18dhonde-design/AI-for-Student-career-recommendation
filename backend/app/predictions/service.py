"""Predictions service — orchestrates ML calls and stores results in MongoDB."""

import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, status

from backend.services.ml.career_service import career_service
from backend.services.ml.cluster_service import cluster_service
from backend.services.ml.placement_service import placement_service
from backend.services.ml.salary_service import salary_service
from backend.services.ml.success_service import success_service

from .repository import predictions_repository
from .schemas import (
    CareerPredictionRequest,
    ClusterPredictionRequest,
    PlacementPredictionRequest,
    SalaryPredictionRequest,
    SuccessPredictionRequest,
)

logger = logging.getLogger(__name__)


def _serialize_prediction(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "user_id": doc["user_id"],
        "prediction_type": doc["prediction_type"],
        "input_data": doc["input_data"],
        "result": doc["result"],
        "created_at": str(doc["created_at"]),
    }


class PredictionsService:
    async def predict_career(self, user_id: str, request: CareerPredictionRequest) -> dict:
        input_data = request.model_dump()
        result = career_service.predict(input_data)
        doc = await predictions_repository.save_prediction(user_id, "career", input_data, result)
        return _serialize_prediction(doc)

    async def predict_salary(self, user_id: str, request: SalaryPredictionRequest) -> dict:
        input_data = request.model_dump()
        result = salary_service.predict(input_data)
        doc = await predictions_repository.save_prediction(user_id, "salary", input_data, result)
        return _serialize_prediction(doc)

    async def predict_placement(self, user_id: str, request: PlacementPredictionRequest) -> dict:
        input_data = request.model_dump()
        result = placement_service.predict(input_data)
        doc = await predictions_repository.save_prediction(user_id, "placement", input_data, result)
        return _serialize_prediction(doc)

    async def predict_success(self, user_id: str, request: SuccessPredictionRequest) -> dict:
        input_data = request.model_dump()
        result = success_service.predict(input_data)
        doc = await predictions_repository.save_prediction(user_id, "success", input_data, result)
        return _serialize_prediction(doc)

    async def predict_cluster(self, user_id: str, request: ClusterPredictionRequest) -> dict:
        input_data = request.model_dump()
        result = cluster_service.predict(input_data)
        doc = await predictions_repository.save_prediction(user_id, "cluster", input_data, result)
        return _serialize_prediction(doc)

    async def get_history(
        self,
        user_id: str,
        prediction_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> tuple:
        docs, total = await predictions_repository.get_history(
            user_id, prediction_type, skip, limit, sort_by, sort_order
        )
        return [_serialize_prediction(d) for d in docs], total

    async def get_prediction(self, prediction_id: str, user_id: str) -> dict:
        doc = await predictions_repository.find_by_id(prediction_id)
        if not doc:
            raise HTTPException(status_code=404, detail="Prediction not found.")
        if doc["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="Access denied.")
        return _serialize_prediction(doc)

    async def delete_prediction(self, prediction_id: str, user_id: str) -> dict:
        deleted = await predictions_repository.delete_prediction(prediction_id, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Prediction not found.")
        return {"message": "Prediction deleted."}


predictions_service = PredictionsService()
