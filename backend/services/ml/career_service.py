"""Career Recommendation ML service wrapper."""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent.parent.parent / "models"

# Career labels mapping (based on common ML training output)
CAREER_LABELS = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Cybersecurity Analyst",
    "Data Analyst",
    "Product Manager",
    "Business Analyst",
    "UI/UX Designer",
    "Embedded Systems Engineer",
    "IoT Engineer",
    "Robotics Engineer",
    "Mobile App Developer",
    "Database Administrator",
    "Network Engineer",
]

# Skill recommendations per career
CAREER_SKILLS = {
    "Software Engineer": ["Python", "Java", "Data Structures", "System Design", "Git"],
    "Data Scientist": ["Python", "Machine Learning", "Statistics", "SQL", "TensorFlow"],
    "Machine Learning Engineer": ["Python", "Deep Learning", "MLOps", "TensorFlow", "PyTorch"],
    "AI Engineer": ["Python", "NLP", "Computer Vision", "LLMs", "PyTorch"],
    "Backend Developer": ["Node.js", "Python", "REST APIs", "Databases", "Docker"],
    "Frontend Developer": ["React", "JavaScript", "CSS", "TypeScript", "Figma"],
    "Full Stack Developer": ["React", "Node.js", "Databases", "REST APIs", "Docker"],
    "Cloud Engineer": ["AWS/GCP/Azure", "Terraform", "Kubernetes", "Networking", "Linux"],
    "DevOps Engineer": ["CI/CD", "Docker", "Kubernetes", "Linux", "Monitoring"],
    "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "SIEM", "Python", "Cryptography"],
    "Data Analyst": ["SQL", "Python", "Excel", "Power BI/Tableau", "Statistics"],
    "Product Manager": ["Agile", "Roadmapping", "Analytics", "Communication", "UX Basics"],
    "Business Analyst": ["SQL", "Excel", "BPMN", "Requirements Analysis", "Stakeholder Mgmt"],
    "UI/UX Designer": ["Figma", "User Research", "Prototyping", "Adobe XD", "HTML/CSS"],
    "Embedded Systems Engineer": ["C/C++", "RTOS", "Microcontrollers", "PCB Design", "Assembly"],
    "IoT Engineer": ["Python", "MQTT", "Embedded C", "Cloud Platforms", "Networking"],
    "Robotics Engineer": ["ROS", "Python", "C++", "Control Systems", "Sensor Integration"],
    "Mobile App Developer": ["Flutter", "React Native", "Swift", "Kotlin", "REST APIs"],
    "Database Administrator": ["SQL", "MongoDB", "PostgreSQL", "Performance Tuning", "Backup & Recovery"],
    "Network Engineer": ["Cisco", "TCP/IP", "Routing & Switching", "Network Security", "Firewalls"],
}


class CareerService:
    """Wraps the career_recommendation.pkl model for predictions."""

    def __init__(self):
        self._model = None
        self._scaler = None
        self._encoder = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        try:
            self._model = joblib.load(MODELS_DIR / "career_recommendation.pkl")
            self._scaler = joblib.load(MODELS_DIR / "career_scaler.pkl")
            # career_encoder.pkl may be None/placeholder (5 bytes)
            enc = joblib.load(MODELS_DIR / "career_encoder.pkl")
            self._encoder = enc if enc is not None else {}
            self._loaded = True
            logger.info("✅ Career model loaded")
        except Exception as exc:
            logger.error("❌ Failed to load career model: %s", exc)
            raise

    def _encode_input(self, data: Dict[str, Any]) -> pd.DataFrame:
        """Encode categorical features and scale numerics."""
        df = pd.DataFrame([data])

        # Encode categorical columns if encoder is a dict of LabelEncoders
        if isinstance(self._encoder, dict):
            for col, enc in self._encoder.items():
                if col in df.columns:
                    try:
                        df[col] = enc.transform(df[col])
                    except Exception:
                        # Unknown category → use -1 or 0
                        df[col] = 0

        # Map string categoricals manually if no encoder
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
        for col in ["Interests"]:
            if col in df.columns:
                df = df.drop(columns=[col])

        return df

    def predict(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        self._load()
        try:
            df = self._encode_input(input_data)
            scaled = self._scaler.transform(df)
            raw_pred = self._model.predict(scaled)
            predicted_label = str(raw_pred[0])

            # Get probabilities if available
            top_careers = [predicted_label]
            confidence = 0.85

            if hasattr(self._model, "predict_proba"):
                probs = self._model.predict_proba(scaled)[0]
                top_indices = np.argsort(probs)[::-1][:5]
                classes = self._model.classes_
                top_careers = [str(classes[i]) for i in top_indices]
                confidence = float(probs[top_indices[0]])

            primary_career = top_careers[0]
            recommended_skills = CAREER_SKILLS.get(primary_career, ["Python", "Communication", "Problem Solving"])

            return {
                "primary_career": primary_career,
                "top_careers": top_careers[:5],
                "confidence": round(confidence * 100, 2),
                "recommended_skills": recommended_skills,
                "career_description": self._get_description(primary_career),
            }
        except Exception as exc:
            logger.error("Career prediction error: %s", exc)
            # Fallback based on field
            return self._rule_based_fallback(input_data)

    def _get_description(self, career: str) -> str:
        descriptions = {
            "Software Engineer": "Design, develop, and maintain software systems and applications.",
            "Data Scientist": "Extract insights from complex datasets using statistical and ML methods.",
            "Machine Learning Engineer": "Build and deploy machine learning models at scale.",
            "AI Engineer": "Develop AI-powered applications and intelligent systems.",
            "Backend Developer": "Build server-side logic, APIs, and database integrations.",
            "Frontend Developer": "Create responsive and interactive user interfaces.",
            "Full Stack Developer": "Handle both frontend and backend development.",
            "Cloud Engineer": "Design and manage cloud infrastructure and services.",
            "DevOps Engineer": "Bridge development and operations for faster delivery.",
            "Cybersecurity Analyst": "Protect systems and networks from cyber threats.",
        }
        return descriptions.get(career, f"Build expertise and advance your career as a {career}.")

    def _rule_based_fallback(self, data: Dict) -> Dict:
        field = str(data.get("field_studied", "")).lower()
        career_map = {
            "computer science": "Software Engineer",
            "information technology": "Backend Developer",
            "electronics": "Embedded Systems Engineer",
            "mechanical": "Robotics Engineer",
            "civil": "Data Analyst",
            "mathematics": "Data Scientist",
            "business": "Business Analyst",
            "management": "Product Manager",
        }
        career = career_map.get(field, "Software Engineer")
        return {
            "primary_career": career,
            "top_careers": [career],
            "confidence": 60.0,
            "recommended_skills": CAREER_SKILLS.get(career, ["Python", "Communication"]),
            "career_description": self._get_description(career),
        }


career_service = CareerService()
