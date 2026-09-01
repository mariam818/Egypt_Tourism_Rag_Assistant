import pytest

from fastapi.testclient import TestClient

from app.main import app


# ============================================================
# Test FastAPI endpoints
# ============================================================

@pytest.fixture
def client():

    # Using TestClient as a context manager ensures that
    # FastAPI's lifespan/startup events are executed.
    with TestClient(app) as test_client:
        yield test_client


# ============================================================
# Test 1 — Health endpoint
# ============================================================

def test_health(client):

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"

    assert data["retrieval"] == "ready"

    assert data["generation"] == "ready"


# ============================================================
# Test 2 — Invalid empty question
# ============================================================

def test_query_empty_question(client):

    response = client.post(
        "/query",
        json={
            "question": ""
        }
    )

    assert response.status_code == 422


# ============================================================
# Test 3 — Missing question field
# ============================================================

def test_query_missing_question(client):

    response = client.post(
        "/query",
        json={}
    )

    assert response.status_code == 422


# ============================================================
# Test 4 — Valid RAG query
# ============================================================

def test_query_valid_question(client):

    response = client.post(
        "/query",
        json={
            "question": (
                "What are some important attractions "
                "to visit in Cairo?"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data

    assert "sources" in data

    assert isinstance(
        data["answer"],
        str
    )

    assert len(data["answer"]) > 0

    assert isinstance(
        data["sources"],
        list
    )

    assert len(data["sources"]) > 0