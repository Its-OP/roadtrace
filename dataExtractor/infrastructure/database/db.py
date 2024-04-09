from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from sqlalchemy.orm import sessionmaker as Sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database

from entities.Base import Base


class UnitOfWork:
    def __init__(self, host):
        self._DATABASE_URI = f'postgresql://admin:admin@{host}:5432/roadtrace'
        engine = create_engine(self._DATABASE_URI, echo=True)
        Base.metadata.bind = engine
        self._engine = engine
        self._sessionmaker = Sessionmaker(bind=self._engine)

    @contextmanager
    def open_session(self) -> Iterator[Session]:
        """Provide a transactional scope around a series of operations."""
        session = self._sessionmaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session(self) -> Session:
        sessionmaker = Sessionmaker(bind=self._engine)
        session = sessionmaker()
        return session

    def commit_session(self, session: Session):
        session.commit()
        session.close()

    def ensure_migrated(self):
        if not database_exists(self._DATABASE_URI):
            create_database(self._DATABASE_URI)

        alembic_cfg = Config('./alembic.ini')
        command.upgrade(alembic_cfg, 'head')
