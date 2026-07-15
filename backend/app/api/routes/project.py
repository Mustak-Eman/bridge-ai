from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from app.api.dependencies import ProjectServiceDep
from app.schemas import (
    PaginationParams,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)


router = APIRouter(
    tags=["Projects"],
)


@router.post(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
)
def create_project(
    workspace_id: UUID,
    payload: ProjectCreate,
    service: ProjectServiceDep,
):
    return service.create_project(
        workspace_id,
        payload,
    )


@router.get(
    "/workspaces/{workspace_id}/projects",
    response_model=ProjectListResponse,
    summary="List projects for a workspace",
)
def list_projects(
    workspace_id: UUID,
    service: ProjectServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> ProjectListResponse:
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
    )

    return service.list_projects(
        workspace_id,
        pagination,
    )


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Get a project",
)
def get_project(
    project_id: UUID,
    service: ProjectServiceDep,
):
    return service.get_project(project_id)


@router.patch(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
)
def update_project(
    project_id: UUID,
    payload: ProjectUpdate,
    service: ProjectServiceDep,
):
    return service.update_project(
        project_id,
        payload,
    )


@router.delete(
    "/projects/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
)
def delete_project(
    project_id: UUID,
    service: ProjectServiceDep,
) -> Response:
    service.delete_project(project_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )