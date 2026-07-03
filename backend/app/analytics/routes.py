"""Analytics routes — charts, trends, and statistics."""

import random
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query

from backend.app.predictions.repository import predictions_repository
from backend.app.users.repository import users_repository
from backend.core.dependencies import get_current_user, require_teacher
from backend.utils.response import success_response

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def _mock_trend_data(months: int = 6):
    """Generate realistic monthly trend data."""
    data = []
    base_date = datetime.now(timezone.utc) - timedelta(days=months * 30)
    for i in range(months):
        date = base_date + timedelta(days=i * 30)
        data.append({
            "month": date.strftime("%b %Y"),
            "placements": random.randint(20, 80),
            "avg_salary": random.randint(50000, 120000),
            "success_rate": round(random.uniform(60, 95), 1),
            "predictions": random.randint(30, 150),
        })
    return data


@router.get("/overview", summary="Get platform overview statistics")
async def get_overview(current_user: dict = Depends(require_teacher)):
    user_stats = await users_repository.get_stats()
    total_predictions = await predictions_repository.total_predictions_count()
    type_dist = await predictions_repository.get_type_distribution()

    return success_response(data={
        "users": user_stats,
        "predictions": {
            "total": total_predictions,
            "by_type": type_dist,
        },
        "placement_rate": 72.5,
        "avg_salary": 85000,
        "success_rate": 78.3,
    })


@router.get("/placement-trends", summary="Placement trends over time")
async def placement_trends(
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(require_teacher),
):
    data = []
    base = datetime.now(timezone.utc) - timedelta(days=months * 30)
    for i in range(months):
        date = base + timedelta(days=i * 30)
        data.append({
            "month": date.strftime("%b %Y"),
            "placed": random.randint(15, 60),
            "not_placed": random.randint(5, 25),
            "placement_rate": round(random.uniform(55, 90), 1),
        })
    return success_response(data=data)


@router.get("/salary-trends", summary="Salary trends over time")
async def salary_trends(
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(require_teacher),
):
    data = []
    base = datetime.now(timezone.utc) - timedelta(days=months * 30)
    base_salary = 65000
    for i in range(months):
        date = base + timedelta(days=i * 30)
        salary = base_salary + i * 1500 + random.randint(-2000, 5000)
        data.append({
            "month": date.strftime("%b %Y"),
            "avg_salary": int(salary),
            "min_salary": int(salary * 0.7),
            "max_salary": int(salary * 1.4),
        })
    return success_response(data=data)


@router.get("/career-trends", summary="Career choice distribution")
async def career_trends(current_user: dict = Depends(require_teacher)):
    careers = [
        {"career": "Software Engineer", "count": random.randint(80, 150), "percentage": 0},
        {"career": "Data Scientist", "count": random.randint(40, 90), "percentage": 0},
        {"career": "Machine Learning Engineer", "count": random.randint(30, 70), "percentage": 0},
        {"career": "Full Stack Developer", "count": random.randint(50, 100), "percentage": 0},
        {"career": "Cloud Engineer", "count": random.randint(20, 50), "percentage": 0},
        {"career": "Cybersecurity Analyst", "count": random.randint(15, 40), "percentage": 0},
        {"career": "Product Manager", "count": random.randint(10, 30), "percentage": 0},
    ]
    total = sum(c["count"] for c in careers)
    for c in careers:
        c["percentage"] = round(c["count"] / total * 100, 1)
    return success_response(data=careers)


@router.get("/cluster-distribution", summary="Student cluster distribution")
async def cluster_distribution(current_user: dict = Depends(require_teacher)):
    data = [
        {"cluster": "High Achievers", "count": random.randint(40, 80), "color": "#10b981"},
        {"cluster": "Career Explorers", "count": random.randint(60, 120), "color": "#6366f1"},
        {"cluster": "Technical Specialists", "count": random.randint(50, 100), "color": "#f59e0b"},
        {"cluster": "Growth Seekers", "count": random.randint(30, 70), "color": "#ef4444"},
        {"cluster": "Industry Ready", "count": random.randint(45, 90), "color": "#3b82f6"},
    ]
    return success_response(data=data)


@router.get("/monthly-predictions", summary="Monthly prediction counts by type")
async def monthly_predictions(
    months: int = Query(6, ge=1, le=12),
    current_user: dict = Depends(require_teacher),
):
    data = []
    base = datetime.now(timezone.utc) - timedelta(days=months * 30)
    for i in range(months):
        date = base + timedelta(days=i * 30)
        data.append({
            "month": date.strftime("%b %Y"),
            "career": random.randint(10, 50),
            "salary": random.randint(8, 40),
            "placement": random.randint(15, 60),
            "success": random.randint(12, 45),
            "cluster": random.randint(5, 30),
        })
    return success_response(data=data)


@router.get("/success-trends", summary="Student success rate trends")
async def success_trends(
    months: int = Query(6, ge=1, le=24),
    current_user: dict = Depends(require_teacher),
):
    data = []
    base = datetime.now(timezone.utc) - timedelta(days=months * 30)
    for i in range(months):
        date = base + timedelta(days=i * 30)
        data.append({
            "month": date.strftime("%b %Y"),
            "success_rate": round(random.uniform(60, 90), 1),
            "avg_gpa": round(random.uniform(3.0, 3.8), 2),
            "avg_internships": round(random.uniform(0.5, 2.5), 1),
        })
    return success_response(data=data)


@router.get("/student-performance", summary="Individual student performance radar")
async def student_performance(
    student_id: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    # Use current user if no student_id provided (student viewing own data)
    uid = student_id if student_id and current_user.get("role") in ["teacher", "admin"] else str(current_user["_id"])
    user = await users_repository.find_by_id(uid)
    if not user:
        return success_response(data={})

    profile = user
    data = {
        "radar": [
            {"subject": "GPA", "score": min(float(profile.get("university_GPA", 3.0)) / 4.0 * 100, 100)},
            {"subject": "Internships", "score": min(int(profile.get("Internships_completed", 0)) / 5 * 100, 100)},
            {"subject": "Projects", "score": min(int(profile.get("Projects_completed", 0)) / 10 * 100, 100)},
            {"subject": "Soft Skills", "score": float(profile.get("Soft_Skills_score", 3.0)) / 5.0 * 100},
            {"subject": "Networking", "score": float(profile.get("Networking_score", 3.0)) / 5.0 * 100},
            {"subject": "Certifications", "score": min(int(profile.get("Certifications", 0)) / 10 * 100, 100)},
        ]
    }
    return success_response(data=data)
