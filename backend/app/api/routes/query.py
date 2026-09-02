
import logging

from fastapi import APIRouter, HTTPException, Request

from app.schemas.query import QueryRequest, QueryResponse


# Router

router = APIRouter()

logger = logging.getLogger(__name__)


# Health Check

@router.get("/health")
async def health_check(request: Request):
    """
    Check whether the RAG backend is running
    and its main services have been initialized.
    """

    retrieval_service = getattr(
        request.app.state,
        "retrieval_service",
        None
    )

    generation_service = getattr(
        request.app.state,
        "generation_service",
        None
    )

    if (
        retrieval_service is None
        or generation_service is None
    ):
        return {
            "status": "unhealthy",
            "message": "RAG services are not initialized."
        }

    return {
        "status": "healthy",
        "service": "Egypt Tourism RAG API",
        "retrieval": "ready",
        "generation": "ready"
    }


# RAG Query Endpoint

@router.post(
    "/query",
    response_model=QueryResponse
)
async def query_rag(
    request_data: QueryRequest,
    request: Request
):
    """
    Process a user question using the RAG pipeline.

    Flow:

    1. Receive question
    2. Retrieve relevant chunks from ChromaDB
    3. Send retrieved context to Ollama
    4. Generate grounded answer
    5. Return answer + sources
    """

    question = request_data.question.strip()

    # --------------------------------------------------------
    # Validate question
    # --------------------------------------------------------

    if not question:

        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty."
        )

    # --------------------------------------------------------
    # Get services initialized during startup
    # --------------------------------------------------------

    retrieval_service = getattr(
        request.app.state,
        "retrieval_service",
        None
    )

    generation_service = getattr(
        request.app.state,
        "generation_service",
        None
    )

    if retrieval_service is None:

        logger.error(
            "Retrieval service is not initialized."
        )

        raise HTTPException(
            status_code=503,
            detail="Retrieval service is unavailable."
        )

    if generation_service is None:

        logger.error(
            "Generation service is not initialized."
        )

        raise HTTPException(
            status_code=503,
            detail="Generation service is unavailable."
        )

    try:

        # STEP 1 — RETRIEVAL

        logger.info(
            "Retrieving context for question: %s",
            question
        )

        retrieved_chunks = (
            retrieval_service.retrieve(
                question
            )
        )

        if not retrieved_chunks:

            return QueryResponse(

                answer=(
                    "I don't have enough information "
                    "in the provided documents to answer "
                    "this question."
                ),

                sources=[]
            )

        logger.info(
            "Retrieved %d chunks.",
            len(retrieved_chunks)
        )


        # STEP 2 — GENERATION

        logger.info(
            "Generating answer using Ollama..."
        )

        answer = generation_service.generate(

            question=question,

            retrieved_chunks=retrieved_chunks
        )


        # STEP 3 — BUILD SOURCES

        sources = []

        for chunk in retrieved_chunks:

            citation = chunk.get(
                "rank",
                len(sources) + 1
            )

            source = chunk.get(
                "source",
                "Unknown source"
            )

            page = chunk.get(
                "page",
                "Unknown"
            )

            chunk_id = chunk.get(
                "chunk_id",
                "Unknown"
            )

            sources.append(
                f"[{citation}] "
                f"{source} "
                f"(Page {page}, Chunk {chunk_id})"
            )


        # STEP 4 — RETURN RESPONSE

        return QueryResponse(

            answer=answer,

            sources=sources
        )


    except RuntimeError as e:

        logger.exception(
            "Generation error."
        )

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )


    except Exception as e:

        logger.exception(
            "Unexpected error while processing query."
        )

        raise HTTPException(

            status_code=500,

            detail=(
                "An unexpected error occurred "
                "while processing the question."
            )
        )
