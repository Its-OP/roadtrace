from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from sqlalchemy_utils import database_exists, create_database


class UnitOfWork:
    def __init__(self):
        self._DATABASE_URI = 'postgresql://admin:admin@localhost:5432/roadtrace'
        self._engine = create_engine(self._DATABASE_URI, echo=True)

    def ensure_migrated(self):
        if not database_exists(self._DATABASE_URI):
            create_database(self._DATABASE_URI)

        alembic_cfg = Config('./alembic.ini')
        command.upgrade(alembic_cfg, 'head')
