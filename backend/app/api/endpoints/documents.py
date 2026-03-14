"""Document upload endpoint: saves file + indexes into ChromaDB."""
import os
from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Document, Employee
from app.schemas.schemas import DocumentOut
from app.services.ingestion import save_file, ingest_document
from app.api.deps import get_current_employee

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentOut, status_code=201)
async def upload_document(
    title: str = Form(...),
    category: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_emp: Employee = Depends(get_current_employee),
):
    allowed = {".pdf", ".txt", ".md", ".docx"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed:
        raise HTTPException(400, f"File type '{ext}' not supported. Use: {allowed}")

    content = await file.read()
    file_path = save_file(content, file.filename)

    doc = Document(title=title, category=category, file_path=file_path, author_id=current_emp.id)
    db.add(doc); db.commit(); db.refresh(doc)

    chunks = ingest_document(file_path, file.filename, doc.id, title, current_emp.id)
    print(f"[Upload] '{title}' indexed: {chunks} chunks")

    return doc


@router.get("/", response_model=list[DocumentOut])
def list_documents(db: Session = Depends(get_db), _: Employee = Depends(get_current_employee)):
    return db.query(Document).order_by(Document.upload_date.desc()).all()
