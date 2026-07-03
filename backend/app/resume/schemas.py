"""Resume schemas."""

from typing import List, Optional
from pydantic import BaseModel, Field


class ResumePersonalInfo(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    summary: Optional[str] = None


class ResumeEducation(BaseModel):
    institution: str
    degree: str
    field: str
    start_year: int
    end_year: Optional[int] = None
    gpa: Optional[float] = None


class ResumeExperience(BaseModel):
    company: str
    role: str
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    description: str
    achievements: List[str] = []


class ResumeProject(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None
    github: Optional[str] = None


class ResumeCertification(BaseModel):
    name: str
    issuer: str
    issued_date: Optional[str] = None
    url: Optional[str] = None


class CreateResumeRequest(BaseModel):
    personal_info: ResumePersonalInfo
    education: List[ResumeEducation] = []
    experience: List[ResumeExperience] = []
    skills: List[str] = []
    projects: List[ResumeProject] = []
    certifications: List[ResumeCertification] = []
    languages: List[str] = []
    template: str = Field(default="modern", description="Template: modern, classic, minimal")


class UpdateResumeRequest(BaseModel):
    personal_info: Optional[ResumePersonalInfo] = None
    education: Optional[List[ResumeEducation]] = None
    experience: Optional[List[ResumeExperience]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[ResumeProject]] = None
    certifications: Optional[List[ResumeCertification]] = None
    languages: Optional[List[str]] = None
    template: Optional[str] = None


class ResumeAnalyzeRequest(BaseModel):
    career_target: str
    current_skills: List[str] = []
    resume_text: Optional[str] = None
