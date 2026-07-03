"""Users/Profile Pydantic schemas."""

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class EducationEntry(BaseModel):
    institution: str = Field(..., min_length=2)
    degree: str
    field: str
    start_year: int
    end_year: Optional[int] = None
    gpa: Optional[float] = None


class ExperienceEntry(BaseModel):
    company: str
    role: str
    start_date: str
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[str] = None


class ProjectEntry(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None
    github: Optional[str] = None


class CertificationEntry(BaseModel):
    name: str
    issuer: str
    issued_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_url: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=500)
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    education: Optional[List[EducationEntry]] = None
    experience: Optional[List[ExperienceEntry]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[ProjectEntry]] = None
    certifications: Optional[List[CertificationEntry]] = None
    interests: Optional[List[str]] = None


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    avatar: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None
    education: List[dict] = []
    experience: List[dict] = []
    skills: List[str] = []
    projects: List[dict] = []
    certifications: List[dict] = []
    interests: List[str] = []
    created_at: str
    updated_at: str
