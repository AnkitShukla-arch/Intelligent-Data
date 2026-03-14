"""Central API router."""
from fastapi import APIRouter
from app.api.endpoints import auth, documents, worklogs, projects, chat

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(documents.router)
api_router.include_router(worklogs.router)
api_router.include_router(projects.router)
api_router.include_router(chat.router)
