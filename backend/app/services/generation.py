import logging

import ollama


logger = logging.getLogger(__name__)


class GenerationService:

    def __init__(
        self,
        model_name: str = "llama3.2",
        host: str = "http://localhost:11434"
    ):
        self.model_name = model_name

        # Create Ollama client once at startup
        self.client = ollama.Client(
            host=host
        )

    def build_prompt(
        self,
        question: str,
        retrieved_chunks: list[dict]
    ) -> str:

        context_parts = []

        for chunk in retrieved_chunks:

            citation = f"[{chunk['rank']}]"

            source = chunk.get(
                "source",
                "Unknown source"
            )

            page = chunk.get(
                "page",
                "Unknown"
            )

            text = chunk.get(
                "text",
                ""
            )

            context_parts.append(
                f"""
SOURCE {citation}

Document: {source}
Page: {page}

Content:
{text}

END SOURCE {citation}
"""
            )

        context = "\n".join(context_parts)

        prompt = f"""
    You are an Egypt tourism assistant.

    Answer the user's question using ONLY the information
    contained in the sources below.

    ========================
    STRICT GROUNDING RULES
    ========================

    1. Use ONLY the provided sources.
    Do not use your own knowledge.

    2. Do NOT invent facts, attractions, dates, prices,
    locations, opening hours, recommendations, or other
    information that is not supported by the sources.

    3. Every factual claim must have a citation immediately
    after the claim.

    4. Citations MUST use ONLY this exact format:

    [1]
    [2]
    [3]
    [4]
    [5]

    5. NEVER write "SOURCE [1]", "Source [1]", "SOURCE 1",
    "Source 1", or any similar wording.

    6. Write citations directly after the relevant statement.

    CORRECT:
    The Giza Plateau is one of Egypt's most famous sites [2].

    CORRECT:
    The Egyptian Museum is located in Cairo [2][4].

    INCORRECT:
    According to SOURCE [2], the Giza Plateau is famous.

    INCORRECT:
    According to Source [2], the Giza Plateau is famous.

    7. A citation number refers to the SOURCE with the
    same number.

    8. NEVER write page numbers in the answer.

    9. NEVER create citation numbers that do not exist
    in the provided sources.

    10. If multiple sources support a statement, cite all
        relevant sources, for example:

        [1][4]

    11. If the sources do not contain enough information
        to answer the question, respond exactly:

        I don't have enough information in the provided
        documents to answer this question.

    12. Do not guess or fill missing information using
        general knowledge.

    13. Keep the answer concise and natural.

    14. Do not mention embeddings, ChromaDB, vector databases,
        retrieval, prompts, or the RAG system.

    15. Do not mention the source labels themselves in the
        answer. Only use the citation numbers [1], [2], etc.

    ========================
    AVAILABLE SOURCES
    ========================

    {context}

    ========================
    USER QUESTION
    ========================

    {question}

    ========================
    ANSWER
    ========================

    Write the answer now.

    IMPORTANT:
    Use citations like [1] and [2] directly after factual
    statements.

    NEVER write "SOURCE [1]" or "According to SOURCE [1]".

    NEVER write page numbers.

    ONLY use citation numbers that exist in the available sources.
    """

        return prompt

    def generate(
        self,
        question: str,
        retrieved_chunks: list[dict]
    ) -> str:

        if not retrieved_chunks:

            return (
                "I don't have enough information in the "
                "provided documents to answer this question."
            )

        prompt = self.build_prompt(
            question,
            retrieved_chunks
        )

        try:

            response = self.client.chat(

                model=self.model_name,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a grounded Egypt tourism "
                            "assistant. You must answer strictly "
                            "from the provided sources and use "
                            "source-number citations."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0.0
                }
            )

            answer = response["message"]["content"]

            return answer.strip()

        except Exception as e:

            logger.exception(
                "Ollama generation failed."
            )

            raise RuntimeError(
                "Failed to generate answer using Ollama: "
                f"{str(e)}"
            )