from pathlib import Path
from typing import Any

import chromadb
from sentence_transformers import SentenceTransformer


class RetrievalService:

    def __init__(
        self,
        vector_store_path: str,
        collection_name: str,
        embedding_model_name: str,
        top_k: int = 5
    ):

        self.vector_store_path = Path(
            vector_store_path
        )

        self.collection_name = (
            collection_name
        )

        self.embedding_model_name = (
            embedding_model_name
        )

        self.top_k = top_k

        # ---------------------------------
        # Load embedding model ONCE
        # ---------------------------------

        self.embedding_model = (
            SentenceTransformer(
                self.embedding_model_name
            )
        )

        # ---------------------------------
        # Connect to persistent ChromaDB
        # ---------------------------------

        self.client = (
            chromadb.PersistentClient(
                path=str(
                    self.vector_store_path
                )
            )
        )

        # ---------------------------------
        # Load existing collection
        # ---------------------------------

        self.collection = (
            self.client.get_collection(
                name=self.collection_name
            )
        )

    def retrieve(
        self,
        question: str,
        top_k: int | None = None
    ) -> list[dict[str, Any]]:

        question = question.strip()

        if not question:

            return []

        k = (
            top_k
            if top_k is not None
            else self.top_k
        )

        # ---------------------------------
        # Embed question
        # ---------------------------------

        question_embedding = (
            self.embedding_model.encode(
                [question],
                normalize_embeddings=True
            )[0]
        )

        # ---------------------------------
        # Search Chroma
        # ---------------------------------

        results = self.collection.query(

            query_embeddings=[
                question_embedding.tolist()
            ],

            n_results=k,

            include=[
                "documents",
                "metadatas",
                "distances"
            ]
        )

        documents = (
            results.get(
                "documents",
                [[]]
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]]
            )[0]
        )

        distances = (
            results.get(
                "distances",
                [[]]
            )[0]
        )

        ids = (
            results.get(
                "ids",
                [[]]
            )[0]
        )

        retrieved = []

        for i in range(
            len(documents)
        ):

            metadata = metadatas[i]

            retrieved.append({

                "rank":
                    i + 1,

                "chunk_id":
                    ids[i],

                "text":
                    documents[i],

                "source":
                    metadata.get(
                        "source"
                    ),

                "page":
                    metadata.get(
                        "page"
                    ),

                "chunk_index":
                    metadata.get(
                        "chunk_index"
                    ),

                "distance":
                    float(
                        distances[i]
                    )
            })

        return retrieved