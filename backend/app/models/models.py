"""Star Schema Models for Corporate Knowledge Nexus.

Dimensions: Employee, Project, Document
Fact:       WorkLog
"""
from datetime import date, datetime
from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    Float, Text, Boolean, ForeignKey
)
from sqlalchemy.orm import relationship
from app.db.session import Base


# ── Dimension Tables ──────────────────────────────────────────────────────────

class Employee(Base):
    __tablename__ = "dim_employee"

    id         = Column(Integer, primary_key=True, index=True)
    full_name  = Column(String(120), nullable=False)
    email      = Column(String(160), unique=True, index=True, nullable=False)
    hashed_pw  = Column(String(256), nullable=False)
    department = Column(String(80))
    role       = Column(String(80))           # e.g. "Senior Dev", "Intern"
    join_date  = Column(Date, default=date.today)
    skills     = Column(Text, default="[]")   # JSON array string
    is_active  = Column(Boolean, default=True)
    is_admin   = Column(Boolean, default=False)

    work_logs         = relationship("WorkLog", back_populates="employee", foreign_keys="WorkLog.employee_id")
    managed_projects  = relationship("Project", back_populates="manager")
    authored_docs     = relationship("Document", back_populates="author")


class Project(Base):
    __tablename__ = "dim_project"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(200), nullable=False, index=True)
    description = Column(Text)
    start_date  = Column(Date)
    end_date    = Column(Date)
    status      = Column(String(30), default="Active")  # Active / Completed / On Hold
    manager_id  = Column(Integer, ForeignKey("dim_employee.id"), nullable=True)

    manager   = relationship("Employee", back_populates="managed_projects")
    work_logs = relationship("WorkLog", back_populates="project")


class Document(Base):
    __tablename__ = "dim_document"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String(300), nullable=False, index=True)
    file_path   = Column(String(500), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    category    = Column(String(80))        # HR / Tech / Sales / Process
    version     = Column(Integer, default=1)
    author_id   = Column(Integer, ForeignKey("dim_employee.id"), nullable=True)

    author    = relationship("Employee", back_populates="authored_docs")
    work_logs = relationship("WorkLog", back_populates="document")


# ── Fact Table ────────────────────────────────────────────────────────────────

class WorkLog(Base):
    __tablename__ = "fact_worklog"

    id              = Column(Integer, primary_key=True, index=True)
    employee_id     = Column(Integer, ForeignKey("dim_employee.id"), nullable=False)
    project_id      = Column(Integer, ForeignKey("dim_project.id"), nullable=False)
    document_id     = Column(Integer, ForeignKey("dim_document.id"), nullable=True)
    log_date        = Column(Date, default=date.today)

    # Measures
    hours_logged    = Column(Float, default=0.0)
    tasks_completed = Column(Integer, default=0)

    # Qualitative fields
    description     = Column(Text, nullable=False)
    status_update   = Column(String(40), default="On Track")   # On Track / Delayed / Blocked
    blockers        = Column(Text, default="")

    employee  = relationship("Employee",  back_populates="work_logs", foreign_keys=[employee_id])
    project   = relationship("Project",   back_populates="work_logs")
    document  = relationship("Document",  back_populates="work_logs")
