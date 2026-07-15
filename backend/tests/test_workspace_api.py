from uuid import uuid4

from fastapi.testclient import TestClient


def create_workspace(
    client: TestClient,
    *,
    name: str = "Bronx Community Center",
    slug: str = "bronx-community-center",
) -> dict[str, object]:
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": name,
            "slug": slug,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_workspace_returns_created_workspace(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Bronx Community Center",
            "slug": "bronx-community-center",
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Bronx Community Center"
    assert body["slug"] == "bronx-community-center"
    assert body["id"] is not None
    assert body["created_at"] is not None
    assert body["updated_at"] is not None


def test_create_workspace_rejects_duplicate_slug(
    client: TestClient,
) -> None:
    create_workspace(client)

    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Another Organization",
            "slug": "bronx-community-center",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "workspace_slug_conflict",
            "message": (
                "A workspace with slug "
                "'bronx-community-center' already exists."
            ),
        }
    }


def test_create_workspace_rejects_invalid_slug(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/workspaces",
        json={
            "name": "Bronx Community Center",
            "slug": "Invalid Slug",
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_get_workspace_returns_workspace(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)

    response = client.get(
        f"/api/v1/workspaces/{workspace['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == workspace["id"]


def test_get_workspace_returns_not_found(
    client: TestClient,
) -> None:
    response = client.get(
        f"/api/v1/workspaces/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "workspace_not_found",
            "message": "Workspace not found.",
        }
    }


def test_list_workspaces_returns_paginated_results(
    client: TestClient,
) -> None:
    create_workspace(
        client,
        name="Alpha Workspace",
        slug="alpha-workspace",
    )
    create_workspace(
        client,
        name="Beta Workspace",
        slug="beta-workspace",
    )
    create_workspace(
        client,
        name="Gamma Workspace",
        slug="gamma-workspace",
    )

    response = client.get(
        "/api/v1/workspaces?page=2&page_size=2"
    )

    assert response.status_code == 200

    body = response.json()

    assert len(body["items"]) == 1
    assert body["items"][0]["name"] == "Gamma Workspace"
    assert body["page"] == 2
    assert body["page_size"] == 2
    assert body["total"] == 3
    assert body["pages"] == 2


def test_update_workspace_returns_updated_workspace(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)

    response = client.patch(
        f"/api/v1/workspaces/{workspace['id']}",
        json={
            "name": "Updated Community Center",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Updated Community Center"
    assert body["slug"] == "bronx-community-center"


def test_delete_workspace_returns_no_content(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)

    delete_response = client.delete(
        f"/api/v1/workspaces/{workspace['id']}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/api/v1/workspaces/{workspace['id']}"
    )

    assert get_response.status_code == 404