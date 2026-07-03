"""Resume routes."""

from fastapi import APIRouter, Depends

from backend.core.dependencies import get_current_user
from backend.utils.response import success_response, created_response

from .schemas import CreateResumeRequest, ResumeAnalyzeRequest, UpdateResumeRequest
from .service import resume_service

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.get("/", summary="Get current user's resume")
async def get_resume(current_user: dict = Depends(get_current_user)):
    data = await resume_service.get_resume(str(current_user["_id"]))
    return success_response(data=data, message="Resume retrieved." if data else "No resume found.")


@router.post("/", summary="Create or save resume")
async def save_resume(
    request: CreateResumeRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await resume_service.save_resume(str(current_user["_id"]), request)
    return created_response(data=data, message="Resume saved.")


@router.put("/", summary="Update resume sections")
async def update_resume(
    request: UpdateResumeRequest,
    current_user: dict = Depends(get_current_user),
):
    data = await resume_service.update_resume(str(current_user["_id"]), request)
    return success_response(data=data, message="Resume updated.")


@router.post("/analyze", summary="Analyze resume for ATS score and gaps")
async def analyze_resume(
    request: ResumeAnalyzeRequest,
    current_user: dict = Depends(get_current_user),
):
    data = resume_service.analyze_resume(str(current_user["_id"]), request)
    return success_response(data=data, message="Resume analyzed.")
