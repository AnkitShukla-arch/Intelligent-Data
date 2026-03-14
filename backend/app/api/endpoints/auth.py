"""Auth endpoints: register + login."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Employee
from app.schemas.schemas import EmployeeCreate, EmployeeOut, LoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=EmployeeOut, status_code=201)
def register(data: EmployeeCreate, db: Session = Depends(get_db)):
    if db.query(Employee).filter(Employee.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    emp = Employee(
        full_name=data.full_name,
        email=data.email,
        hashed_pw=get_password_hash(data.password),
        department=data.department,
        role=data.role,
        skills=data.skills,
    )
    db.add(emp); db.commit(); db.refresh(emp)
    return emp


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.email == data.email).first()
    if not emp or not verify_password(data.password, emp.hashed_pw):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(emp.id)})
    return {"access_token": token, "employee": emp}
