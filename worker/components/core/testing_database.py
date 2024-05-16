"""
Module providing functionality for 
creating SQLite in-memory sessions.
"""

import contextlib
from sqlalchemy import create_engine, orm

from components.core import database


@contextlib.contextmanager
def create_sqlite_inmemory_session():
    """
    Context manager for creating an SQLite in-memory session.

    This context manager creates an SQLite database
    in memory, initializes the necessary tables
    using SQLAlchemy Base.metadata, and provides a
    session for database operations. After
    the context block, it cleans up by closing the
    session, dropping all tables, and disposing
    of the engine.

    Yields:
        sqlalchemy.orm.Session: A session object
        for interacting with the in-memory SQLite database.

    """
    engine = create_engine("sqlite:///:memory:", echo=False)

    database.Base.metadata.create_all(bind=engine)
    session_maker = orm.sessionmaker(bind=engine, expire_on_commit=False)

    session = session_maker()

    try:
        yield session

    finally:
        session.close()
        database.Base.metadata.drop_all(bind=engine)
        engine.dispose()
