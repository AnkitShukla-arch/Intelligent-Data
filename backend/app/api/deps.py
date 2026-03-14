"""Dependency: extract current employee from JWT token."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Employee
from app.core.security import decode_access_token

bearer = HTTPBearer(auto_error=False)


def get_current_employee(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> Employee:
    if not creds:
        raise HTTPException(status_code=401, detail="Not authenticated")
    payload = decode_access_token(creds.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    emp = db.get(Employee, int(payload["sub"]))
    if not emp or not emp.is_active:
        raise HTTPException(status_code=401, detail="User not found")
    return emp
