from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Project
from app.repositories.base import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository[Project]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Project)

    def list_for_workspace(
        self,
        workspace_id: UUID,
        *,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.workspace_id == workspace_id)
            .order_by(
                Project.name,
                Project.id,
            )
            .offset(offset)
            .limit(limit)
        )

        return list(self._session.scalars(statement))

    def count_for_workspace(
        self,
        workspace_id: UUID,
    ) -> int:
        statement = (
            select(func.count())
            .select_from(Project)
            .where(Project.workspace_id == workspace_id)
        )

        return self._session.scalar(statement) or 0