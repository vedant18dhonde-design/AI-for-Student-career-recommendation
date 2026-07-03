"""Student Success Prediction ML service wrapper."""

import logging
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models"


class SuccessService:
    """Wraps the success_model.pkl for student success prediction."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoders = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        try:
            self._model = joblib.load(MODELS_DIR / "success_model.pkl")
            self._scaler = joblib.load(MODELS_DIR / "scaler_success.pkl")
            self._encoders = joblib.load(MODELS_DIR / "encoder_success.pkl")
            self._loaded = True
            logger.info("✅ Success model loaded")
        except Exception as exc:
            logger.error("❌ Failed to load success model: %s", exc)
            raise

    def _encode_input(self, data: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame([data])

        if isinstance(self._encoders, dict):
            for col, enc in self._encoders.items():
                if col in df.columns:
                    try:
                        df[col] = enc.transform(df[col].astype(str))
                    except Exception:
                        df[col] = 0

        gender_map = {"male": 0, "female": 1, "other": 2}
        if "gender" in df.columns and df["gender"].dtype == object:
            df["gender"] = df["gender"].str.lower().map(gender_map).fillna(0)

        field_map = {
            "computer science": 0, "information technology": 1, "electronics": 2,
            "mechanical": 3, "civil": 4, "mathematics": 5, "physics": 6,
            "business": 7, "management": 8, "arts": 9,
        }
        if "field_studied" in df.columns and df["field_studied"].dtype == object:
            df["field_studied"] = df["field_studied"].str.lower().map(field_map).fillna(0)

        for col in ["Interests", "career_goal"]:
            if col in df.columns:
                df = df.drop(columns=[col])

        return df

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._load()
        try:
            df = self._encode_input(input_data)
            scaled = self._scaler.transform(df)
            prediction = self._model.predict(scaled)
            raw = prediction[0]

            # Handle both binary classification and regression outputs
            if isinstance(raw, (bool, np.bool_)):
                success = bool(raw)
                score = 85.0 if success else 40.0
            elif isinstance(raw, (int, np.integer)):
                success = bool(raw)
                score = 85.0 if success else 40.0
            else:
                score = float(raw)
                success = score >= 0.5

            if hasattr(self._model, "predict_proba"):
                probs = self._model.predict_proba(scaled)[0]
                score = float(probs[1] if len(probs) > 1 else probs[0]) * 100

            grade = (
                "Excellent" if score >= 80 else
                "Good" if score >= 60 else
                "Average" if score >= 40 else
                "Needs Improvement"
            )

            return {
                "success": success,
                "success_score": round(score, 2),
                "grade": grade,
                "label": "High Success Potential" if success else "Growth Opportunity",
                "strong_areas": self._get_strong_areas(input_data),
                "improvement_areas": self._get_weak_areas(input_data),
            }
        except Exception as exc:
            logger.error("Success prediction error: %s", exc)
            return self._rule_based_fallback(input_data)

    def _get_strong_areas(self, data: Dict) -> list:
        strong = []
        if float(data.get("university_GPA", 0)) >= 3.5:
            strong.append("Academic Performance")
        if int(data.get("Internships_completed", 0)) >= 2:
            strong.append("Industry Experience")
        if int(data.get("Projects_completed", 0)) >= 3:
            strong.append("Project Portfolio")
        if float(data.get("Soft_Skills_score", 0)) >= 4.0:
            strong.append("Soft Skills")
        if int(data.get("Certifications", 0)) >= 3:
            strong.append("Certifications")
        if float(data.get("Networking_score", 0)) >= 4.0:
            strong.append("Professional Networking")
        return strong or ["Determination"]

    def _get_weak_areas(self, data: Dict) -> list:
        weak = []
        if float(data.get("university_GPA", 0)) < 3.0:
            weak.append("Academic Performance")
        if int(data.get("Internships_completed", 0)) == 0:
            weak.append("Industry Experience")
        if int(data.get("Projects_completed", 0)) < 2:
            weak.append("Project Portfolio")
        if float(data.get("Soft_Skills_score", 0)) < 3.0:
            weak.append("Soft Skills")
        if int(data.get("Certifications", 0)) == 0:
            weak.append("Certifications")
        return weak or ["Keep up the great work!"]

    def _rule_based_fallback(self, data: Dict) -> Dict:
        score = 0
        score += min(float(data.get("university_GPA", 0)) / 4.0, 1.0) * 35
        score += min(int(data.get("Internships_completed", 0)) / 3.0, 1.0) * 20
        score += min(int(data.get("Projects_completed", 0)) / 5.0, 1.0) * 20
        score += min(float(data.get("Soft_Skills_score", 0)) / 5.0, 1.0) * 15
        score += min(int(data.get("Certifications", 0)) / 5.0, 1.0) * 10
        success = score >= 50
        grade = "Excellent" if score >= 80 else "Good" if score >= 60 else "Average" if score >= 40 else "Needs Improvement"
        return {
            "success": success,
            "success_score": round(score, 2),
            "grade": grade,
            "label": "High Success Potential" if success else "Growth Opportunity",
            "strong_areas": self._get_strong_areas(data),
            "improvement_areas": self._get_weak_areas(data),
        }


success_service = SuccessService()
