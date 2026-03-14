"""Work log CRUD + analytics."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import WorkLog, Employee, Project
from app.schemas.schemas import WorkLogCreate, WorkLogOut, WorkLogStats
from app.api.deps import get_current_employee

router = APIRouter(prefix="/worklogs", tags=["worklogs"])


@router.post("/", response_model=WorkLogOut, status_code=201)
def create_worklog(
    data: WorkLogCreate,
    db: Session = Depends(get_db),
    emp: Employee = Depends(get_current_employee),
):
    if not db.get(Project, data.project_id):
        raise HTTPException(404, "Project not found")
    wl = WorkLog(**data.model_dump(), employee_id=emp.id)
    db.add(wl); db.commit(); db.refresh(wl)
    return wl


@router.get("/", response_model=List[WorkLogOut])
def list_worklogs(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    _: Employee = Depends(get_current_employee),
):
    q = db.query(WorkLog)
    if project_id:
        q = q.filter(WorkLog.project_id == project_id)
    return q.order_by(WorkLog.log_date.desc()).limit(100).all()


@router.get("/stats", response_model=WorkLogStats)
def worklog_stats(
    db: Session = Depends(get_db),
    _: Employee = Depends(get_current_employee),
):
    total = db.query(func.count(WorkLog.id)).scalar()
    hours = db.query(func.sum(WorkLog.hours_logged)).scalar() or 0.0
    blocked = db.query(func.count(WorkLog.id)).filter(WorkLog.status_update == "Blocked").scalar()
    on_track = db.query(func.count(WorkLog.id)).filter(WorkLog.status_update == "On Track").scalar()
    delayed = db.query(func.count(WorkLog.id)).filter(WorkLog.status_update == "Delayed").scalar()
    return WorkLogStats(
        total_logs=total, total_hours=round(hours, 2),
        blocked_count=blocked, on_track_count=on_track, delayed_count=delayed
    )
