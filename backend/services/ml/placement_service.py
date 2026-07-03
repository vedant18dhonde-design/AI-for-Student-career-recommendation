"""Placement Prediction ML service wrapper."""

import logging
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models"


class PlacementService:
    """Wraps the placement_model.pkl for placement prediction."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoders = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        try:
            self._model = joblib.load(MODELS_DIR / "placement_model.pkl")
            self._scaler = joblib.load(MODELS_DIR / "placement_scaler.pkl")
            self._encoders = joblib.load(MODELS_DIR / "placemnet_encoder.pkl")
            self._loaded = True
            logger.info("✅ Placement model loaded")
        except Exception as exc:
            logger.error("❌ Failed to load placement model: %s", exc)
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
            placed = bool(prediction[0])

            probability = 0.5
            if hasattr(self._model, "predict_proba"):
                probs = self._model.predict_proba(scaled)[0]
                probability = float(probs[1]) if len(probs) > 1 else float(probs[0])

            readiness = "High" if probability >= 0.7 else "Medium" if probability >= 0.4 else "Low"

            return {
                "placed": placed,
                "placement_probability": round(probability * 100, 2),
                "readiness_level": readiness,
                "label": "Likely to be Placed" if placed else "Needs Improvement",
                "tips": self._get_tips(placed, probability, input_data),
            }
        except Exception as exc:
            logger.error("Placement prediction error: %s", exc)
            return self._rule_based_fallback(input_data)

    def _get_tips(self, placed: bool, prob: float, data: Dict) -> list:
        tips = []
        if float(data.get("university_GPA", 0)) < 3.0:
            tips.append("Improve your GPA to above 3.0 for better placement chances.")
        if int(data.get("Internships_completed", 0)) == 0:
            tips.append("Complete at least one internship to gain industry experience.")
        if int(data.get("Projects_completed", 0)) < 2:
            tips.append("Build 2-3 strong projects to showcase your skills.")
        if int(data.get("Certifications", 0)) == 0:
            tips.append("Earn relevant certifications to strengthen your profile.")
        if float(data.get("Soft_Skills_score", 0)) < 3.5:
            tips.append("Work on communication and teamwork skills.")
        if not tips:
            tips.append("Keep maintaining your excellent profile!" if placed else "Continue improving your skills.")
        return tips[:4]

    def _rule_based_fallback(self, data: Dict) -> Dict:
        score = 0
        score += min(float(data.get("university_GPA", 0)) / 4.0, 1.0) * 30
        score += min(int(data.get("Internships_completed", 0)) / 3.0, 1.0) * 25
        score += min(int(data.get("Projects_completed", 0)) / 5.0, 1.0) * 20
        score += min(int(data.get("Certifications", 0)) / 5.0, 1.0) * 15
        score += min(float(data.get("Soft_Skills_score", 0)) / 5.0, 1.0) * 10
        placed = score >= 50
        return {
            "placed": placed,
            "placement_probability": round(score, 2),
            "readiness_level": "High" if score >= 70 else "Medium" if score >= 40 else "Low",
            "label": "Likely to be Placed" if placed else "Needs Improvement",
            "tips": self._get_tips(placed, score / 100, data),
        }


placement_service = PlacementService()
