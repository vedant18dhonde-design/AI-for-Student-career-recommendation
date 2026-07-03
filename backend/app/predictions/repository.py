"""Predictions repository — MongoDB operations for prediction history."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from bson import ObjectId

from backend.core.database import Collections, get_collection

logger = logging.getLogger(__name__)


class PredictionsRepository:
    @property
    def predictions(self):
        return get_collection(Collections.PREDICTIONS)

    async def save_prediction(
        self,
        user_id: str,
        prediction_type: str,
        input_data: dict,
        result: dict,
    ) -> dict:
        doc = {
            "user_id": user_id,
            "prediction_type": prediction_type,
            "input_data": input_data,
            "result": result,
            "created_at": datetime.now(timezone.utc),
        }
        inserted = await self.predictions.insert_one(doc)
        doc["_id"] = inserted.inserted_id
        return doc

    async def find_by_id(self, prediction_id: str) -> Optional[dict]:
        try:
            return await self.predictions.find_one({"_id": ObjectId(prediction_id)})
        except Exception:
            return None

    async def get_history(
        self,
        user_id: str,
        prediction_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> Tuple[List[dict], int]:
        query: dict = {"user_id": user_id}
        if prediction_type:
            query["prediction_type"] = prediction_type

        total = await self.predictions.count_documents(query)
        cursor = (
            self.predictions.find(query)
            .sort(sort_by, sort_order)
            .skip(skip)
            .limit(limit)
        )
        docs = await cursor.to_list(length=limit)
        return docs, total

    async def delete_prediction(self, prediction_id: str, user_id: str) -> bool:
        result = await self.predictions.delete_one({
            "_id": ObjectId(prediction_id),
            "user_id": user_id,
        })
        return result.deleted_count > 0

    async def get_type_distribution(self, user_id: Optional[str] = None) -> dict:
        match = {"$match": {"user_id": user_id}} if user_id else {"$match": {}}
        pipeline = [
            match,
            {"$group": {"_id": "$prediction_type", "count": {"$sum": 1}}},
        ]
        cursor = self.predictions.aggregate(pipeline)
        docs = await cursor.to_list(length=100)
        return {d["_id"]: d["count"] for d in docs}

    async def get_monthly_counts(self, months: int = 6) -> List[dict]:
        pipeline = [
            {
                "$group": {
                    "_id": {
                        "year": {"$year": "$created_at"},
                        "month": {"$month": "$created_at"},
                        "type": "$prediction_type",
                    },
                    "count": {"$sum": 1},
                }
            },
            {"$sort": {"_id.year": 1, "_id.month": 1}},
            {"$limit": months * 5},
        ]
        cursor = self.predictions.aggregate(pipeline)
        return await cursor.to_list(length=200)

    async def total_predictions_count(self) -> int:
        return await self.predictions.count_documents({})

    async def recent_predictions(self, limit: int = 10) -> List[dict]:
        cursor = self.predictions.find({}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)


predictions_repository = PredictionsRepository()
