"""FastAPI application entry point."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router
from app.db.session import engine, Base

# Auto-create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Corporate Knowledge Nexus — RAG + LLM + NLQ system",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Restrict to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["root"])
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": f"{settings.API_V1_STR}/docs",
    }


@app.get("/health", tags=["root"])
def health():
    return {"status": "ok"}
