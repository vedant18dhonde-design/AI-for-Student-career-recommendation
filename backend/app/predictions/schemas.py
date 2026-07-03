"""Predictions Pydantic schemas — input validation and response models."""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class StudentProfileInput(BaseModel):
    """Shared input schema across all 5 ML models."""
    age: int = Field(..., ge=16, le=60)
    gender: Literal["male", "female", "other"]
    field_studied: str = Field(..., min_length=2)
    university_GPA: float = Field(..., ge=0.0, le=4.0)
    Internships_completed: int = Field(..., ge=0, le=20)
    Projects_completed: int = Field(..., ge=0, le=50)
    Certifications: int = Field(..., ge=0, le=30)
    Soft_Skills_score: float = Field(..., ge=0.0, le=5.0)
    Networking_score: float = Field(..., ge=0.0, le=5.0)
    Interests: Optional[str] = None

    @field_validator("field_studied")
    @classmethod
    def normalize_field(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("gender")
    @classmethod
    def normalize_gender(cls, v: str) -> str:
        return v.lower()


class CareerPredictionRequest(StudentProfileInput):
    pass


class SalaryPredictionRequest(StudentProfileInput):
    pass


class PlacementPredictionRequest(StudentProfileInput):
    pass


class SuccessPredictionRequest(StudentProfileInput):
    pass


class ClusterPredictionRequest(StudentProfileInput):
    pass


class PredictionResponse(BaseModel):
    id: str
    user_id: str
    prediction_type: str
    input_data: Dict[str, Any]
    result: Dict[str, Any]
    created_at: str


class PredictionHistoryFilter(BaseModel):
    prediction_type: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
