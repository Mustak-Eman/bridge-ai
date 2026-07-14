from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Workspace
from app.repositories.base import SQLAlchemyRepository


class WorkspaceRepository(SQLAlchemyRepository[Workspace]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Workspace)

    def get_by_slug(self, slug: str) -> Workspace | None:
        statement = select(Workspace).where(
            Workspace.slug == slug
        )

        return self._session.scalar(statement)

    def list_all(self) -> list[Workspace]:
        statement = select(Workspace).order_by(
            Workspace.name
        )

        return list(self._session.scalars(statement))