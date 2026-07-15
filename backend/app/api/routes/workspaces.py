from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from app.api.dependencies import WorkspaceServiceDep
from app.schemas import (
    PaginationParams,
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceResponse,
    WorkspaceUpdate,
)


router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a workspace",
)
def create_workspace(
    payload: WorkspaceCreate,
    service: WorkspaceServiceDep,
):
    return service.create_workspace(payload)


@router.get(
    "",
    response_model=WorkspaceListResponse,
    summary="List workspaces",
)
def list_workspaces(
    service: WorkspaceServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
) -> WorkspaceListResponse:
    pagination = PaginationParams(
        page=page,
        page_size=page_size,
    )

    return service.list_workspaces(pagination)


@router.get(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Get a workspace",
)
def get_workspace(
    workspace_id: UUID,
    service: WorkspaceServiceDep,
):
    return service.get_workspace(workspace_id)


@router.patch(
    "/{workspace_id}",
    response_model=WorkspaceResponse,
    summary="Update a workspace",
)
def update_workspace(
    workspace_id: UUID,
    payload: WorkspaceUpdate,
    service: WorkspaceServiceDep,
):
    return service.update_workspace(
        workspace_id,
        payload,
    )


@router.delete(
    "/{workspace_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a workspace",
)
def delete_workspace(
    workspace_id: UUID,
    service: WorkspaceServiceDep,
) -> Response:
    service.delete_workspace(workspace_id)

    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )