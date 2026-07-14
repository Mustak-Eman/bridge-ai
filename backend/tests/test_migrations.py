from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect


def create_alembic_config(database_url: str) -> Config:
    backend_dir = Path(__file__).resolve().parents[1]
    config_path = backend_dir / "alembic.ini"

    config = Config(str(config_path))
    config.set_main_option(
        "script_location",
        str(backend_dir / "alembic"),
    )
    config.set_main_option(
        "sqlalchemy.url",
        database_url.replace("%", "%%"),
    )

    return config


def test_migrations_upgrade_and_downgrade(tmp_path: Path) -> None:
    database_path = tmp_path / "migration_test.db"
    database_url = f"sqlite:///{database_path.as_posix()}"

    alembic_config = create_alembic_config(database_url)

    command.upgrade(alembic_config, "head")

    engine = create_engine(database_url)

    try:
        table_names = inspect(engine).get_table_names()

        assert "alembic_version" in table_names
        assert "workspaces" in table_names
        assert "projects" in table_names
    finally:
        engine.dispose()

    command.downgrade(alembic_config, "base")

    engine = create_engine(database_url)

    try:
        table_names = inspect(engine).get_table_names()

        assert "workspaces" not in table_names
        assert "projects" not in table_names
    finally:
        engine.dispose()

    command.upgrade(alembic_config, "head")

    engine = create_engine(database_url)

    try:
        table_names = inspect(engine).get_table_names()

        assert "workspaces" in table_names
        assert "projects" in table_names
    finally:
        engine.dispose()