from fastapi.testclient import TestClient


def test_application_exception_returns_standard_error(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/test-error")

    assert response.status_code == 400

    assert response.json() == {
        "error": {
            "code": "test_error",
            "message": "This is a test application error.",
        }
    }