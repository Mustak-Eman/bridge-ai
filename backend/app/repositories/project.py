from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Project
from app.repositories.base import SQLAlchemyRepository


class ProjectRepository(SQLAlchemyRepository[Project]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Project)

    def list_for_workspace(
        self,
        workspace_id: UUID,
    ) -> list[Project]:
        statement = (
            select(Project)
            .where(Project.workspace_id == workspace_id)
            .order_by(Project.name)
        )

        return list(self._session.scalars(statement))