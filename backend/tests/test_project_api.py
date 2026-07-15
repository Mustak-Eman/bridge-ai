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


def create_project(
    client: TestClient,
    workspace_id: object,
    *,
    name: str = "Benefits Navigation",
    description: str | None = (
        "Helps residents identify available benefits."
    ),
) -> dict[str, object]:
    response = client.post(
        f"/api/v1/workspaces/{workspace_id}/projects",
        json={
            "name": name,
            "description": description,
        },
    )

    assert response.status_code == 201

    return response.json()


def test_create_project_returns_created_project(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)

    response = client.post(
        f"/api/v1/workspaces/{workspace['id']}/projects",
        json={
            "name": "Benefits Navigation",
            "description": (
                "Helps residents identify available benefits."
            ),
        },
    )

    assert response.status_code == 201

    body = response.json()

    assert body["workspace_id"] == workspace["id"]
    assert body["name"] == "Benefits Navigation"
    assert body["description"] == (
        "Helps residents identify available benefits."
    )
    assert body["id"] is not None


def test_create_project_rejects_missing_workspace(
    client: TestClient,
) -> None:
    response = client.post(
        f"/api/v1/workspaces/{uuid4()}/projects",
        json={
            "name": "Benefits Navigation",
            "description": None,
        },
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == (
        "workspace_not_found"
    )


def test_get_project_returns_project(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)
    project = create_project(
        client,
        workspace["id"],
    )

    response = client.get(
        f"/api/v1/projects/{project['id']}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == project["id"]


def test_get_project_returns_not_found(
    client: TestClient,
) -> None:
    response = client.get(
        f"/api/v1/projects/{uuid4()}"
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "project_not_found",
            "message": "Project not found.",
        }
    }


def test_list_projects_returns_only_parent_projects(
    client: TestClient,
) -> None:
    first_workspace = create_workspace(client)
    second_workspace = create_workspace(
        client,
        name="Other Workspace",
        slug="other-workspace",
    )

    create_project(
        client,
        first_workspace["id"],
        name="Benefits Navigation",
        description=None,
    )
    create_project(
        client,
        first_workspace["id"],
        name="Document Intake",
        description=None,
    )
    create_project(
        client,
        second_workspace["id"],
        name="Housing Support",
        description=None,
    )

    response = client.get(
        (
            "/api/v1/workspaces/"
            f"{first_workspace['id']}/projects"
        )
    )

    assert response.status_code == 200

    body = response.json()

    assert [
        project["name"]
        for project in body["items"]
    ] == [
        "Benefits Navigation",
        "Document Intake",
    ]
    assert body["total"] == 2
    assert body["pages"] == 1


def test_list_projects_rejects_missing_workspace(
    client: TestClient,
) -> None:
    response = client.get(
        f"/api/v1/workspaces/{uuid4()}/projects"
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == (
        "workspace_not_found"
    )


def test_update_project_returns_updated_project(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)
    project = create_project(
        client,
        workspace["id"],
    )

    response = client.patch(
        f"/api/v1/projects/{project['id']}",
        json={
            "name": "Updated Benefits Navigation",
            "description": None,
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["name"] == "Updated Benefits Navigation"
    assert body["description"] is None
    assert body["workspace_id"] == workspace["id"]


def test_delete_project_returns_no_content(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)
    project = create_project(
        client,
        workspace["id"],
    )

    delete_response = client.delete(
        f"/api/v1/projects/{project['id']}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/api/v1/projects/{project['id']}"
    )

    assert get_response.status_code == 404


def test_deleting_workspace_cascades_to_projects(
    client: TestClient,
) -> None:
    workspace = create_workspace(client)
    project = create_project(
        client,
        workspace["id"],
    )

    delete_response = client.delete(
        f"/api/v1/workspaces/{workspace['id']}"
    )

    assert delete_response.status_code == 204

    project_response = client.get(
        f"/api/v1/projects/{project['id']}"
    )

    assert project_response.status_code == 404