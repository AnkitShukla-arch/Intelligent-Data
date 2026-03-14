"""Project CRUD endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Project, Employee
from app.schemas.schemas import ProjectCreate, ProjectOut
from app.api.deps import get_current_employee

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectOut, status_code=201)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    emp: Employee = Depends(get_current_employee),
):
    proj = Project(**data.model_dump(), manager_id=emp.id)
    db.add(proj); db.commit(); db.refresh(proj)
    return proj


@router.get("/", response_model=List[ProjectOut])
def list_projects(db: Session = Depends(get_db), _: Employee = Depends(get_current_employee)):
    return db.query(Project).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db), _: Employee = Depends(get_current_employee)):
    p = db.get(Project, project_id)
    if not p:
        raise HTTPException(404, "Project not found")
    return p
