"""Seed script: creates a default admin account and a sample project."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal, engine, Base
from app.models.models import Employee, Project
from app.core.security import get_password_hash
from datetime import date

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Admin employee
if not db.query(Employee).filter(Employee.email == "admin@company.com").first():
    admin = Employee(
        full_name="Admin User",
        email="admin@company.com",
        hashed_pw=get_password_hash("admin123"),
        department="IT",
        role="Admin",
        skills='["management","AI"]',
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print("✅ Admin created: admin@company.com / admin123")

    # Sample project
    proj = Project(
        name="Knowledge Nexus Rollout",
        description="Initial rollout of the corporate RAG system.",
        start_date=date.today(),
        status="Active",
        manager_id=admin.id,
    )
    db.add(proj)
    db.commit()
    print("✅ Sample project created.")
else:
    print("ℹ️  Admin already exists.")

db.close()
