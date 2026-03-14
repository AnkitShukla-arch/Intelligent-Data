from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # Project
    PROJECT_NAME: str = "Corporate Knowledge Nexus"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_USE_A_LONG_RANDOM_STRING"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Database
    DATABASE_URL: str = "sqlite:///./know_net_pro.db"

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # ChromaDB
    CHROMA_DB_DIR: str = "./chroma_db"

    # Uploads
    UPLOAD_DIR: str = "./uploaded_docs"


settings = Settings()
