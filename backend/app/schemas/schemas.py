"""Pydantic v2 schemas for request/response validation."""
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, EmailStr


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    department: str
    role: str
    skills: str = "[]"


class EmployeeOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    full_name: str
    email: str
    department: str
    role: str
    join_date: date
    skills: str
    is_admin: bool


# ── Project ───────────────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    name: str
    description: str = ""
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str = "Active"


class ProjectOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    name: str
    description: str
    start_date: Optional[date]
    end_date: Optional[date]
    status: str


# ── Document ──────────────────────────────────────────────────────────────────

class DocumentOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    title: str
    category: str
    upload_date: datetime
    version: int
    author_id: Optional[int]


# ── WorkLog ───────────────────────────────────────────────────────────────────

class WorkLogCreate(BaseModel):
    project_id: int
    hours_logged: float = 0.0
    tasks_completed: int = 0
    description: str
    status_update: str = "On Track"
    blockers: str = ""
    document_id: Optional[int] = None


class WorkLogOut(BaseModel):
    model_config = {"from_attributes": True}
    id: int
    employee_id: int
    project_id: int
    document_id: Optional[int]
    log_date: date
    hours_logged: float
    tasks_completed: int
    description: str
    status_update: str
    blockers: str


# ── Auth ──────────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee: EmployeeOut


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str
    fresher_mode: bool = False


class ChatResponse(BaseModel):
    answer: str
    sources: List[str] = []


# ── Analytics ─────────────────────────────────────────────────────────────────

class WorkLogStats(BaseModel):
    total_logs: int
    total_hours: float
    blocked_count: int
    on_track_count: int
    delayed_count: int
