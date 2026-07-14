from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.orm import Session

from app.database.base import Base


ModelT = TypeVar("ModelT", bound=Base)


class SQLAlchemyRepository(Generic[ModelT]):
    def __init__(
        self,
        session: Session,
        model_type: type[ModelT],
    ) -> None:
        self._session = session
        self._model_type = model_type

    def get(self, entity_id: UUID) -> ModelT | None:
        return self._session.get(self._model_type, entity_id)

    def add(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        self._session.flush()

        return entity

    def delete(self, entity: ModelT) -> None:
        self._session.delete(entity)
        self._session.flush()