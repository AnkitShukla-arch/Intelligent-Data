"""NLQ / RAG chat endpoint."""
from fastapi import APIRouter, Depends
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.rag import answer_query
from app.models.models import Employee
from app.api.deps import get_current_employee

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    _: Employee = Depends(get_current_employee),
):
    result = answer_query(req.query, req.fresher_mode)
    return ChatResponse(**result)
