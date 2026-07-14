from collections.abc import Generator
from pathlib import Path

import pytest
from sqlalchemy import Engine, text
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.database.session import create_database_engine


@pytest.fixture
def sqlite_settings(tmp_path: Path) -> Settings:
    database_path = tmp_path / "test.db"

    return Settings(
        environment="testing",
        debug=False,
        database_url=f"sqlite:///{database_path.as_posix()}",
        database_echo=False,
    )


@pytest.fixture
def engine(
    sqlite_settings: Settings,
) -> Generator[Engine, None, None]:
    database_engine = create_database_engine(sqlite_settings)

    yield database_engine

    database_engine.dispose()


def test_database_engine_connects(engine: Engine) -> None:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    assert result.scalar_one() == 1


def test_sqlite_foreign_keys_are_enabled(engine: Engine) -> None:
    with engine.connect() as connection:
        result = connection.execute(text("PRAGMA foreign_keys"))

    assert result.scalar_one() == 1


def test_session_can_execute_query(engine: Engine) -> None:
    with Session(engine) as session:
        result = session.execute(text("SELECT 1"))

    assert result.scalar_one() == 1