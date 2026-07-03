"""Recommendations routes."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import get_current_user
from backend.utils.response import success_response

from .service import recommendations_service

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("/courses", summary="Get course recommendations")
async def get_courses(
    career: str = Query(..., description="Target career"),
    skills: Optional[str] = Query(None, description="Comma-separated student skills"),
    current_user: dict = Depends(get_current_user),
):
    skill_list = [s.strip() for s in skills.split(",")] if skills else []
    data = recommendations_service.get_courses(career, skill_list)
    return success_response(data=data)


@router.get("/jobs", summary="Get job recommendations")
async def get_jobs(
    career: str = Query(..., description="Target career"),
    current_user: dict = Depends(get_current_user),
):
    data = recommendations_service.get_jobs(career)
    return success_response(data=data)


@router.get("/internships", summary="Get internship recommendations")
async def get_internships(
    career: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    data = recommendations_service.get_internships(career)
    return success_response(data=data)


@router.get("/companies", summary="Get company recommendations")
async def get_companies(
    career: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    data = recommendations_service.get_companies(career)
    return success_response(data=data)


@router.get("/skill-gap", summary="Get skill gap analysis")
async def get_skill_gap(
    career: str = Query(...),
    skills: Optional[str] = Query(None, description="Comma-separated current skills"),
    current_user: dict = Depends(get_current_user),
):
    skill_list = [s.strip() for s in skills.split(",")] if skills else []
    # Also pull skills from user profile
    profile_skills = current_user.get("skills", [])
    all_skills = list(set(skill_list + profile_skills))
    data = recommendations_service.get_skill_gap(career, all_skills)
    return success_response(data=data)


@router.get("/roadmap", summary="Get personalized learning roadmap")
async def get_roadmap(
    career: str = Query(...),
    gpa: float = Query(3.0),
    internships: int = Query(0),
    placement_probability: float = Query(50.0),
    current_user: dict = Depends(get_current_user),
):
    data = recommendations_service.get_learning_roadmap(career, gpa, internships, placement_probability)
    return success_response(data=data)
