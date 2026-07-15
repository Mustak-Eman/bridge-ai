from collections.abc import Generator

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models import Project, Workspace
from app.repositories import ProjectRepository, WorkspaceRepository


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


def test_workspace_repository_adds_and_retrieves_by_slug(
    session: Session,
) -> None:
    repository = WorkspaceRepository(session)

    workspace = repository.add(
        Workspace(
            name="Bronx Community Center",
            slug="bronx-community-center",
        )
    )

    saved_workspace = repository.get_by_slug(
        "bronx-community-center"
    )

    assert workspace.id is not None
    assert saved_workspace is not None
    assert saved_workspace.id == workspace.id


def test_repository_does_not_commit_automatically(
    engine: Engine,
) -> None:
    with Session(engine, expire_on_commit=False) as first_session:
        repository = WorkspaceRepository(first_session)

        repository.add(
            Workspace(
                name="Uncommitted Workspace",
                slug="uncommitted-workspace",
            )
        )

        first_session.rollback()

    with Session(engine) as second_session:
        repository = WorkspaceRepository(second_session)

        saved_workspace = repository.get_by_slug(
            "uncommitted-workspace"
        )

        assert saved_workspace is None


def test_project_repository_lists_projects_for_workspace(
    session: Session,
) -> None:
    workspace_repository = WorkspaceRepository(session)
    project_repository = ProjectRepository(session)

    first_workspace = workspace_repository.add(
        Workspace(
            name="First Workspace",
            slug="first-workspace",
        )
    )

    second_workspace = workspace_repository.add(
        Workspace(
            name="Second Workspace",
            slug="second-workspace",
        )
    )

    project_repository.add(
        Project(
            workspace_id=first_workspace.id,
            name="Benefits Navigation",
            description=None,
        )
    )

    project_repository.add(
        Project(
            workspace_id=first_workspace.id,
            name="Document Intake",
            description=None,
        )
    )

    project_repository.add(
        Project(
            workspace_id=second_workspace.id,
            name="Housing Support",
            description=None,
        )
    )

    projects = project_repository.list_for_workspace(
        first_workspace.id
    )

    assert [project.name for project in projects] == [
        "Benefits Navigation",
        "Document Intake",
    ]
    
def test_workspace_repository_lists_paginated_results(
    session: Session,
) -> None:
    repository = WorkspaceRepository(session)

    for name, slug in [
        ("Alpha Workspace", "alpha-workspace"),
        ("Beta Workspace", "beta-workspace"),
        ("Gamma Workspace", "gamma-workspace"),
    ]:
        repository.add(
            Workspace(
                name=name,
                slug=slug,
            )
        )

    workspaces = repository.list_paginated(
        offset=1,
        limit=1,
    )

    assert len(workspaces) == 1
    assert workspaces[0].name == "Beta Workspace"


def test_workspace_repository_counts_workspaces(
    session: Session,
) -> None:
    repository = WorkspaceRepository(session)

    repository.add(
        Workspace(
            name="First Workspace",
            slug="first-workspace",
        )
    )
    repository.add(
        Workspace(
            name="Second Workspace",
            slug="second-workspace",
        )
    )

    assert repository.count() == 2


def test_project_repository_counts_projects_for_workspace(
    session: Session,
) -> None:
    workspace_repository = WorkspaceRepository(session)
    project_repository = ProjectRepository(session)

    workspace = workspace_repository.add(
        Workspace(
            name="Workspace",
            slug="workspace",
        )
    )

    project_repository.add(
        Project(
            workspace_id=workspace.id,
            name="First Project",
            description=None,
        )
    )
    project_repository.add(
        Project(
            workspace_id=workspace.id,
            name="Second Project",
            description=None,
        )
    )

    assert (
        project_repository.count_for_workspace(workspace.id)
        == 2
    )