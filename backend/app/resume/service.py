"""Resume service — builder, preview, and ATS analyzer."""

import logging
from typing import Dict, List, Optional

from backend.app.recommendations.service import SKILLS_TREE

from .repository import resume_repository
from .schemas import CreateResumeRequest, ResumeAnalyzeRequest, UpdateResumeRequest

logger = logging.getLogger(__name__)

ATS_KEYWORDS = {
    "Software Engineer": ["Python", "Java", "algorithms", "REST API", "microservices", "CI/CD", "agile", "testing"],
    "Data Scientist": ["Python", "machine learning", "statistics", "SQL", "TensorFlow", "pandas", "visualization"],
    "Machine Learning Engineer": ["deep learning", "neural networks", "PyTorch", "MLOps", "model deployment", "feature engineering"],
    "Backend Developer": ["REST APIs", "database", "SQL", "Node.js", "Python", "authentication", "microservices"],
    "default": ["Python", "communication", "teamwork", "problem solving", "git", "agile"],
}


def _serialize_resume(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id", ""))
    return doc


class ResumeService:
    async def get_resume(self, user_id: str) -> Optional[dict]:
        doc = await resume_repository.find_by_user(user_id)
        return _serialize_resume(doc) if doc else None

    async def save_resume(self, user_id: str, request: CreateResumeRequest) -> dict:
        data = request.model_dump()
        doc = await resume_repository.create_or_update(user_id, data)
        return _serialize_resume(doc)

    async def update_resume(self, user_id: str, request: UpdateResumeRequest) -> dict:
        data = request.model_dump(exclude_none=True)
        doc = await resume_repository.create_or_update(user_id, data)
        return _serialize_resume(doc)

    def analyze_resume(self, user_id: str, request: ResumeAnalyzeRequest) -> dict:
        career = request.career_target
        student_skills = [s.lower() for s in request.current_skills]
        resume_text = (request.resume_text or "").lower()

        keywords = ATS_KEYWORDS.get(career, ATS_KEYWORDS["default"])
        required_skills = SKILLS_TREE.get(career, SKILLS_TREE.get("default", {}))
        all_required = list(set(
            required_skills.get("core", []) +
            required_skills.get("technical", []) +
            required_skills.get("soft", [])
        )) if required_skills else keywords

        matched_keywords = [k for k in keywords if k.lower() in resume_text or k.lower() in student_skills]
        missing_keywords = [k for k in keywords if k not in matched_keywords]

        ats_score = round(len(matched_keywords) / len(keywords) * 100, 1) if keywords else 50

        suggestions = []
        if ats_score < 60:
            suggestions.append("Add more industry-specific keywords to pass ATS filters.")
        if len(request.current_skills) < 5:
            suggestions.append("List at least 8-10 technical skills relevant to your target role.")
        if "github" not in resume_text and "projects" not in resume_text:
            suggestions.append("Add a Projects section with GitHub links to showcase your work.")
        if "internship" not in resume_text and "experience" not in resume_text:
            suggestions.append("Include any internship or work experience, even if brief.")
        if len(resume_text) < 200:
            suggestions.append("Expand your resume with more detailed descriptions of achievements.")
        if not suggestions:
            suggestions.append("Your resume looks strong! Keep it concise (1 page for < 5 years experience).")

        return {
            "ats_score": ats_score,
            "career_target": career,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "missing_skills": [s for s in all_required if s.lower() not in student_skills][:8],
            "suggestions": suggestions,
            "grade": "A" if ats_score >= 80 else "B" if ats_score >= 60 else "C" if ats_score >= 40 else "D",
            "recommended_courses": [
                {"name": f"Master {s}", "platform": "Coursera/Udemy", "skill": s}
                for s in missing_keywords[:4]
            ],
        }


resume_service = ResumeService()
