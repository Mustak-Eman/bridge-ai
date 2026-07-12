from fastapi.testclient import TestClient


def test_root(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body == {
        "message": "Bridge AI API",
        "health": "/api/v1/health",
        "docs": "/docs",
        "environment": "development",
    }


def test_health(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    body = response.json()

    assert body == {
        "status": "healthy",
        "service": "bridge-ai-api",
        "version": "0.1.0",
        "environment": "development",
    }