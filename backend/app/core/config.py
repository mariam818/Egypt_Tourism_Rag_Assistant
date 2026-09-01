from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# backend/
BACKEND_DIR = Path(__file__).resolve().parents[2]

# backend/data/vector_store/
VECTOR_STORE_DIR = BACKEND_DIR / "data" / "vector_store"


class Settings(BaseSettings):

    # -------------------------
    # Application
    # -------------------------

    APP_NAME: str = "Egypt Tourism RAG API"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True


    # -------------------------
    # API
    # -------------------------

    API_HOST: str = "0.0.0.0"

    API_PORT: int = 8000


    # -------------------------
    # CORS
    # -------------------------

    FRONTEND_ORIGIN: str = "http://localhost:8501"


    # -------------------------
    # ChromaDB
    # -------------------------

    VECTOR_STORE_PATH: str = str(
        VECTOR_STORE_DIR
    )

    COLLECTION_NAME: str = "egypt_tourism"


    # -------------------------
    # Embeddings
    # -------------------------

    EMBEDDING_MODEL: str = (
        "sentence-transformers/all-MiniLM-L6-v2"
    )


    # -------------------------
    # Retrieval
    # -------------------------

    TOP_K: int = 5


    # -------------------------
    # Ollama
    # -------------------------

    OLLAMA_HOST: str = "http://localhost:11434"

    OLLAMA_MODEL: str = "llama3.2"

    # -------------------------
    # Pydantic settings
    # -------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()