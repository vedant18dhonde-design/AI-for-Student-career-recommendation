"""Salary Prediction ML service wrapper."""

import logging
from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models"


class SalaryService:
    """Wraps the salary_model.pkl for salary prediction."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoders = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        try:
            self._model = joblib.load(MODELS_DIR / "salary_model.pkl")
            self._scaler = joblib.load(MODELS_DIR / "scaler_salary.pkl")
            self._encoders = joblib.load(MODELS_DIR / "enoder_salary.pkl")
            self._loaded = True
            logger.info("✅ Salary model loaded")
        except Exception as exc:
            logger.error("❌ Failed to load salary model: %s", exc)
            raise

    def _encode_input(self, data: Dict[str, Any]) -> pd.DataFrame:
        df = pd.DataFrame([data])

        # Apply stored encoders (dict of LabelEncoders keyed by column name)
        if isinstance(self._encoders, dict):
            for col, enc in self._encoders.items():
                if col in df.columns:
                    try:
                        df[col] = enc.transform(df[col].astype(str))
                    except Exception:
                        df[col] = 0

        # Fallback manual encoding for string cols
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

        # Drop non-numeric text columns
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
            salary = float(prediction[0])

            return {
                "predicted_salary": round(salary, 2),
                "salary_range": {
                    "min": round(salary * 0.85, 2),
                    "max": round(salary * 1.15, 2),
                },
                "currency": "USD",
                "period": "annual",
                "confidence_note": "Estimate based on profile data. Actual salary varies by location and company.",
            }
        except Exception as exc:
            logger.error("Salary prediction error: %s", exc)
            return self._rule_based_fallback(input_data)

    def _rule_based_fallback(self, data: Dict) -> Dict:
        gpa = float(data.get("university_GPA", 3.0))
        internships = int(data.get("Internships_completed", 0))
        certs = int(data.get("Certifications", 0))

        base = 50000
        base += gpa * 5000
        base += internships * 8000
        base += certs * 3000

        return {
            "predicted_salary": round(base, 2),
            "salary_range": {"min": round(base * 0.85, 2), "max": round(base * 1.15, 2)},
            "currency": "USD",
            "period": "annual",
            "confidence_note": "Rule-based estimate. ML model unavailable.",
        }


salary_service = SalaryService()
