import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.query import router as query_router
from app.core.config import settings
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService
from app.utils.logging_config import setup_logging


# ============================================================
# Logging
# ============================================================

logger = setup_logging()


# ============================================================
# Application lifespan
# ============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Starting Egypt Tourism RAG API...")

    try:

        # ----------------------------------------------------
        # Load Retrieval Service ONCE at startup
        # ----------------------------------------------------

        logger.info(
            "Loading embedding model and ChromaDB..."
        )

        app.state.retrieval_service = RetrievalService(

            vector_store_path=settings.VECTOR_STORE_PATH,

            collection_name=settings.COLLECTION_NAME,

            embedding_model_name=settings.EMBEDDING_MODEL,

            top_k=settings.TOP_K
        )

        logger.info(
            "Retrieval service loaded successfully."
        )


        # ----------------------------------------------------
        # Create Ollama Generation Service ONCE
        # ----------------------------------------------------

        logger.info(
            "Connecting to Ollama..."
        )

        app.state.generation_service = GenerationService(

            model_name=settings.OLLAMA_MODEL,

            host=settings.OLLAMA_HOST
        )

        logger.info(
            "Ollama generation service initialized."
        )


        # ----------------------------------------------------
        # Verify Ollama connection
        # ----------------------------------------------------

        try:

            app.state.generation_service.client.list()

            logger.info(
                "Ollama connection verified successfully."
            )

        except Exception as e:

            logger.warning(
                "Could not verify Ollama connection: %s",
                e
            )

            logger.warning(
                "Make sure Ollama is running and "
                "the model '%s' is installed.",
                settings.OLLAMA_MODEL
            )


        logger.info(
            "Egypt Tourism RAG API started successfully."
        )

        yield


    except Exception as e:

        logger.exception(
            "Failed to initialize application: %s",
            e
        )

        raise


    finally:

        logger.info(
            "Shutting down Egypt Tourism RAG API..."
        )


# ============================================================
# FastAPI application
# ============================================================

app = FastAPI(

    title=settings.APP_NAME,

    version=settings.APP_VERSION,

    description=(
        "RAG-powered Egypt Tourism Assistant using "
        "Lonely Planet Egypt documents, ChromaDB, "
        "Sentence Transformers, and Ollama."
    ),

    lifespan=lifespan
)

app.include_router(
    query_router
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        settings.FRONTEND_ORIGIN
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ============================================================
# Root endpoint
# ============================================================

@app.get("/")
async def root():

    return {
        "message": "Egypt Tourism RAG API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }