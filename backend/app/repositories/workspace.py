from sqlalchemy import func, select
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

    def list_paginated(
        self,
        *,
        offset: int,
        limit: int,
    ) -> list[Workspace]:
        statement = (
            select(Workspace)
            .order_by(
                Workspace.name,
                Workspace.id,
            )
            .offset(offset)
            .limit(limit)
        )

        return list(self._session.scalars(statement))

    def count(self) -> int:
        statement = select(func.count()).select_from(Workspace)

        return self._session.scalar(statement) or 0