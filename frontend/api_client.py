import os

import requests
from dotenv import load_dotenv


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

DEFAULT_API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://localhost:8000",
)


# ============================================================
# Health check
# ============================================================

def check_backend_health(api_url=None):

    base = (api_url or DEFAULT_API_BASE_URL).strip().rstrip("/")

    try:

        response = requests.get(
            f"{base}/health",
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"Unable to connect to the backend: {e}"
        )


# ============================================================
# Send question to RAG backend
# ============================================================

def ask_question(question: str, api_url=None):

    if not question or not question.strip():

        raise ValueError(
            "Please enter a question."
        )

    base = (api_url or DEFAULT_API_BASE_URL).strip().rstrip("/")

    try:

        response = requests.post(

            f"{base}/query",

            json={
                "question": question.strip()
            },

            timeout=300
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.Timeout:

        raise RuntimeError(
            "The request took too long. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:

        raise RuntimeError(
            "Could not connect to the RAG backend. "
            "Please make sure FastAPI is running."
        )

    except requests.exceptions.HTTPError as e:

        try:
            detail = response.json().get(
                "detail",
                "Backend returned an error."
            )
        except Exception:
            detail = response.text

        raise RuntimeError(
            f"Backend error ({response.status_code}): "
            f"{detail}"
        )

    except requests.exceptions.RequestException as e:

        raise RuntimeError(
            f"An error occurred while contacting "
            f"the backend: {e}"
        )
