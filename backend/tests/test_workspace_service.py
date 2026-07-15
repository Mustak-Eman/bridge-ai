from collections.abc import Generator
from uuid import uuid4

import pytest
from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session

from app.core.exceptions import (
    WorkspaceNotFoundError,
    WorkspaceSlugConflictError,
)
from app.database.base import Base
from app.models import Workspace
from app.repositories import WorkspaceRepository
from app.schemas import (
    PaginationParams,
    WorkspaceCreate,
    WorkspaceUpdate,
)
from app.services import WorkspaceService


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
def service(session: Session) -> WorkspaceService:
    return WorkspaceService(
        session=session,
        workspace_repository=WorkspaceRepository(session),
    )


def test_create_workspace_commits_workspace(
    service: WorkspaceService,
    session: Session,
) -> None:
    workspace = service.create_workspace(
        WorkspaceCreate(
            name="Bronx Community Center",
            slug="bronx-community-center",
        )
    )

    saved_workspace = session.get(Workspace, workspace.id)

    assert saved_workspace is not None
    assert saved_workspace.slug == "bronx-community-center"


def test_create_workspace_rejects_duplicate_slug(
    service: WorkspaceService,
) -> None:
    payload = WorkspaceCreate(
        name="Bronx Community Center",
        slug="bronx-community-center",
    )

    service.create_workspace(payload)

    with pytest.raises(WorkspaceSlugConflictError):
        service.create_workspace(payload)


def test_get_workspace_raises_when_missing(
    service: WorkspaceService,
) -> None:
    with pytest.raises(WorkspaceNotFoundError):
        service.get_workspace(uuid4())


def test_list_workspaces_returns_pagination_metadata(
    service: WorkspaceService,
) -> None:
    for index in range(3):
        service.create_workspace(
            WorkspaceCreate(
                name=f"Workspace {index}",
                slug=f"workspace-{index}",
            )
        )

    result = service.list_workspaces(
        PaginationParams(
            page=2,
            page_size=2,
        )
    )

    assert len(result.items) == 1
    assert result.page == 2
    assert result.page_size == 2
    assert result.total == 3
    assert result.pages == 2


def test_update_workspace_changes_fields(
    service: WorkspaceService,
) -> None:
    workspace = service.create_workspace(
        WorkspaceCreate(
            name="Original Workspace",
            slug="original-workspace",
        )
    )

    updated_workspace = service.update_workspace(
        workspace.id,
        WorkspaceUpdate(
            name="Updated Workspace",
        ),
    )

    assert updated_workspace.name == "Updated Workspace"
    assert updated_workspace.slug == "original-workspace"


def test_delete_workspace_removes_workspace(
    service: WorkspaceService,
    session: Session,
) -> None:
    workspace = service.create_workspace(
        WorkspaceCreate(
            name="Temporary Workspace",
            slug="temporary-workspace",
        )
    )

    service.delete_workspace(workspace.id)

    assert session.get(Workspace, workspace.id) is None