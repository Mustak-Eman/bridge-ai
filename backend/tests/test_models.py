from sqlalchemy import Engine, create_engine, event, select
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models import Project, Workspace


def create_test_engine() -> Engine:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(
        dbapi_connection: object,
        connection_record: object,
    ) -> None:
        del connection_record

        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine


def test_workspace_and_project_relationship() -> None:
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            workspace = Workspace(
                name="Bronx Community Center",
                slug="bronx-community-center",
            )

            project = Project(
                name="Benefits Navigation",
                description="Support benefit eligibility workflows.",
            )

            workspace.projects.append(project)
            session.add(workspace)
            session.commit()

            saved_workspace = session.scalar(
                select(Workspace).where(
                    Workspace.slug == "bronx-community-center"
                )
            )

            assert saved_workspace is not None
            assert saved_workspace.name == "Bronx Community Center"
            assert len(saved_workspace.projects) == 1
            assert saved_workspace.projects[0].name == "Benefits Navigation"
            assert saved_workspace.projects[0].workspace_id == saved_workspace.id
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


def test_deleting_workspace_deletes_projects() -> None:
    engine = create_test_engine()
    Base.metadata.create_all(engine)

    try:
        with Session(engine) as session:
            workspace = Workspace(
                name="Community Services",
                slug="community-services",
                projects=[
                    Project(
                        name="Document Intake",
                        description=None,
                    )
                ],
            )

            session.add(workspace)
            session.commit()

            project_id = workspace.projects[0].id

            session.delete(workspace)
            session.commit()

            deleted_project = session.get(Project, project_id)

            assert deleted_project is None
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()