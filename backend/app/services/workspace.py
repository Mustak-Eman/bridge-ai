import math
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    WorkspaceNotFoundError,
    WorkspaceSlugConflictError,
)
from app.models import Workspace
from app.repositories import WorkspaceRepository
from app.schemas import (
    PaginationParams,
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceResponse,
    WorkspaceUpdate,
)


class WorkspaceService:
    def __init__(
        self,
        *,
        session: Session,
        workspace_repository: WorkspaceRepository,
    ) -> None:
        self._session = session
        self._workspace_repository = workspace_repository

    def create_workspace(
        self,
        payload: WorkspaceCreate,
    ) -> Workspace:
        existing_workspace = (
            self._workspace_repository.get_by_slug(payload.slug)
        )

        if existing_workspace is not None:
            raise WorkspaceSlugConflictError(payload.slug)

        workspace = Workspace(
            name=payload.name,
            slug=payload.slug,
        )

        try:
            self._workspace_repository.add(workspace)
            self._session.commit()
            self._session.refresh(workspace)
        except IntegrityError as exception:
            self._session.rollback()
            raise WorkspaceSlugConflictError(
                payload.slug
            ) from exception
        except Exception:
            self._session.rollback()
            raise

        return workspace

    def get_workspace(
        self,
        workspace_id: UUID,
    ) -> Workspace:
        workspace = self._workspace_repository.get(workspace_id)

        if workspace is None:
            raise WorkspaceNotFoundError()

        return workspace

    def list_workspaces(
        self,
        pagination: PaginationParams,
    ) -> WorkspaceListResponse:
        workspaces = self._workspace_repository.list_paginated(
            offset=pagination.offset,
            limit=pagination.page_size,
        )
        total = self._workspace_repository.count()

        pages = (
            math.ceil(total / pagination.page_size)
            if total > 0
            else 0
        )

        return WorkspaceListResponse(
            items=[
                WorkspaceResponse.model_validate(workspace)
                for workspace in workspaces
            ],
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
            pages=pages,
        )

    def update_workspace(
        self,
        workspace_id: UUID,
        payload: WorkspaceUpdate,
    ) -> Workspace:
        workspace = self.get_workspace(workspace_id)
        update_data = payload.model_dump(exclude_unset=True)

        new_slug = update_data.get("slug")

        if new_slug is not None and new_slug != workspace.slug:
            existing_workspace = (
                self._workspace_repository.get_by_slug(new_slug)
            )

            if existing_workspace is not None:
                raise WorkspaceSlugConflictError(new_slug)

        for field_name, value in update_data.items():
            setattr(workspace, field_name, value)

        try:
            self._session.commit()
            self._session.refresh(workspace)
        except IntegrityError as exception:
            self._session.rollback()

            conflict_slug = (
                new_slug
                if isinstance(new_slug, str)
                else workspace.slug
            )

            raise WorkspaceSlugConflictError(
                conflict_slug
            ) from exception
        except Exception:
            self._session.rollback()
            raise

        return workspace

    def delete_workspace(
        self,
        workspace_id: UUID,
    ) -> None:
        workspace = self.get_workspace(workspace_id)

        try:
            self._workspace_repository.delete(workspace)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise