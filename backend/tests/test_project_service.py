from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ProjectNotFoundError,
    WorkspaceNotFoundError,
)
from app.database.base import Base
from app.models import Project, Workspace
from app.repositories import (
    ProjectRepository,
    WorkspaceRepository,
)
from app.schemas import (
    PaginationParams,
    ProjectCreate,
    ProjectUpdate,
)
from app.services import ProjectService


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    database_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(database_engine, "connect")
    def enable_foreign_keys(
        dbapi_connection: object,
        connection_record: object,
    ) -> None:
        del connection_record

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    Base.metadata.create_all(database_engine)

    yield database_engine

    Base.metadata.drop_all(database_engine)
    database_engine.dispose()


@pytest.fixture
def session(engine: Engine) -> Generator[Session, None, None]:
    with Session(
        engine,
        autoflush=False,
        expire_on_commit=False,
    ) as database_session:
        yield database_session
        database_session.rollback()


@pytest.fixture
def service(session: Session) -> ProjectService:
    return ProjectService(
        session=session,
        project_repository=ProjectRepository(session),
        workspace_repository=WorkspaceRepository(session),
    )


@pytest.fixture
def workspace(session: Session) -> Workspace:
    repository = WorkspaceRepository(session)

    workspace = repository.add(
        Workspace(
            name="Bronx Community Center",
            slug="bronx-community-center",
        )
    )

    session.commit()

    return workspace


def test_create_project_commits_project(
    service: ProjectService,
    workspace: Workspace,
    session: Session,
) -> None:
    project = service.create_project(
        workspace.id,
        ProjectCreate(
            name="Benefits Navigation",
            description="Helps residents identify available benefits.",
        ),
    )

    saved_project = session.get(Project, project.id)

    assert saved_project is not None
    assert saved_project.workspace_id == workspace.id
    assert saved_project.name == "Benefits Navigation"


def test_create_project_rejects_missing_workspace(
    service: ProjectService,
) -> None:
    with pytest.raises(WorkspaceNotFoundError):
        service.create_project(
            uuid4(),
            ProjectCreate(
                name="Benefits Navigation",
                description=None,
            ),
        )


def test_get_project_raises_when_missing(
    service: ProjectService,
) -> None:
    with pytest.raises(ProjectNotFoundError):
        service.get_project(uuid4())


def test_list_projects_returns_only_workspace_projects(
    service: ProjectService,
    workspace: Workspace,
    session: Session,
) -> None:
    other_workspace = WorkspaceRepository(session).add(
        Workspace(
            name="Other Workspace",
            slug="other-workspace",
        )
    )
    session.commit()

    service.create_project(
        workspace.id,
        ProjectCreate(
            name="Benefits Navigation",
            description=None,
        ),
    )
    service.create_project(
        workspace.id,
        ProjectCreate(
            name="Document Intake",
            description=None,
        ),
    )
    service.create_project(
        other_workspace.id,
        ProjectCreate(
            name="Housing Support",
            description=None,
        ),
    )

    result = service.list_projects(
        workspace.id,
        PaginationParams(
            page=1,
            page_size=20,
        ),
    )

    assert [project.name for project in result.items] == [
        "Benefits Navigation",
        "Document Intake",
    ]
    assert result.total == 2
    assert result.pages == 1


def test_list_projects_rejects_missing_workspace(
    service: ProjectService,
) -> None:
    with pytest.raises(WorkspaceNotFoundError):
        service.list_projects(
            uuid4(),
            PaginationParams(),
        )


def test_update_project_changes_fields(
    service: ProjectService,
    workspace: Workspace,
) -> None:
    project = service.create_project(
        workspace.id,
        ProjectCreate(
            name="Original Project",
            description="Original description.",
        ),
    )

    updated_project = service.update_project(
        project.id,
        ProjectUpdate(
            name="Updated Project",
            description=None,
        ),
    )

    assert updated_project.name == "Updated Project"
    assert updated_project.description is None


def test_delete_project_removes_project(
    service: ProjectService,
    workspace: Workspace,
    session: Session,
) -> None:
    project = service.create_project(
        workspace.id,
        ProjectCreate(
            name="Temporary Project",
            description=None,
        ),
    )

    service.delete_project(project.id)

    assert session.get(Project, project.id) is None