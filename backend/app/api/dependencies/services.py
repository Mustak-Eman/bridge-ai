from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db_session
from app.repositories import (
    ProjectRepository,
    WorkspaceRepository,
)
from app.services import ProjectService, WorkspaceService


DatabaseSessionDep = Annotated[
    Session,
    Depends(get_db_session),
]


def get_workspace_service(
    session: DatabaseSessionDep,
) -> WorkspaceService:
    return WorkspaceService(
        session=session,
        workspace_repository=WorkspaceRepository(session),
    )


def get_project_service(
    session: DatabaseSessionDep,
) -> ProjectService:
    return ProjectService(
        session=session,
        project_repository=ProjectRepository(session),
        workspace_repository=WorkspaceRepository(session),
    )


WorkspaceServiceDep = Annotated[
    WorkspaceService,
    Depends(get_workspace_service),
]

ProjectServiceDep = Annotated[
    ProjectService,
    Depends(get_project_service),
]