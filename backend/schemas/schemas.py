from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


# ── Auth ──────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Resume ────────────────────────────────────────
class ResumeUpsert(BaseModel):
    content: str


class ResumeResponse(BaseModel):
    id: int
    content: str
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Cover Letter ──────────────────────────────────
class GenerateRequest(BaseModel):
    company_name: str
    position: str
    jd_text: str
    resume_text: Optional[str] = None


class CoverLetterSaveRequest(BaseModel):
    company_name: str
    position: str
    jd_text: str
    content: str


class CoverLetterUpdate(BaseModel):
    content: str


class CoverLetterResponse(BaseModel):
    id: int
    company_name: str
    position: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}