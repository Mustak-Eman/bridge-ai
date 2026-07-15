import math
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProjectNotFoundError,
    WorkspaceNotFoundError,
)
from app.models import Project
from app.repositories import (
    ProjectRepository,
    WorkspaceRepository,
)
from app.schemas import (
    PaginationParams,
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)


class ProjectService:
    def __init__(
        self,
        *,
        session: Session,
        project_repository: ProjectRepository,
        workspace_repository: WorkspaceRepository,
    ) -> None:
        self._session = session
        self._project_repository = project_repository
        self._workspace_repository = workspace_repository

    def create_project(
        self,
        workspace_id: UUID,
        payload: ProjectCreate,
    ) -> Project:
        workspace = self._workspace_repository.get(workspace_id)

        if workspace is None:
            raise WorkspaceNotFoundError()

        project = Project(
            workspace_id=workspace.id,
            name=payload.name,
            description=payload.description,
        )

        try:
            self._project_repository.add(project)
            self._session.commit()
            self._session.refresh(project)
        except Exception:
            self._session.rollback()
            raise

        return project

    def get_project(
        self,
        project_id: UUID,
    ) -> Project:
        project = self._project_repository.get(project_id)

        if project is None:
            raise ProjectNotFoundError()

        return project

    def list_projects(
        self,
        workspace_id: UUID,
        pagination: PaginationParams,
    ) -> ProjectListResponse:
        workspace = self._workspace_repository.get(workspace_id)

        if workspace is None:
            raise WorkspaceNotFoundError()

        projects = self._project_repository.list_for_workspace(
            workspace_id,
            offset=pagination.offset,
            limit=pagination.page_size,
        )

        total = self._project_repository.count_for_workspace(
            workspace_id
        )

        pages = (
            math.ceil(total / pagination.page_size)
            if total > 0
            else 0
        )

        return ProjectListResponse(
            items=[
                ProjectResponse.model_validate(project)
                for project in projects
            ],
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
            pages=pages,
        )

    def update_project(
        self,
        project_id: UUID,
        payload: ProjectUpdate,
    ) -> Project:
        project = self.get_project(project_id)
        update_data = payload.model_dump(exclude_unset=True)

        for field_name, value in update_data.items():
            setattr(project, field_name, value)

        try:
            self._session.commit()
            self._session.refresh(project)
        except Exception:
            self._session.rollback()
            raise

        return project

    def delete_project(
        self,
        project_id: UUID,
    ) -> None:
        project = self.get_project(project_id)

        try:
            self._project_repository.delete(project)
            self._session.commit()
        except Exception:
            self._session.rollback()
            raise