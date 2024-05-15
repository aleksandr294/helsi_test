"""
Module for managing database connections and sessions.

This module provides the DatabaseMngr class,
which handles database connections
and provides methods for creating sessions and
managing connections in a context.
"""

import typing
import contextlib
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from components.core import config
from sqlalchemy import orm

Base = orm.declarative_base()
SessionMaker = typing.Callable[[], typing.ContextManager[Session]]
cnfg = config.config


class DatabaseMngr:
    def __init__(
        self, engine: typing.Optional[sqlalchemy.engine.Engine] = None
    ) -> None:
        """
         Initializes a DatabaseMngr instance.

        Args:
            engine (Optional[sqlalchemy.engine.Engine]): The SQLAlchemy engine
            to be used for database connections.

        """
        self.engine = engine

    def get_session(self) -> sessionmaker:
        """
        Creates and returns a sessionmaker
        instance bound to the engine.

        Returns:
            sessionmaker: A sessionmaker instance.

        """
        return sessionmaker(bind=self.engine)

    @contextlib.contextmanager
    def connect(self):
        """
        A context manager for handling database connections.

        Yields:
            Connection: A database connection.

        """
        session_maker = self.get_session()
        with session_maker() as conn:
            yield conn

    instance: typing.Optional[typing.Any] = None

    @staticmethod
    def get_db():
        """
        Retrieves a DatabaseMngr instance.

        If an instance does not exist, creates a new one with the provided engine.

        Returns:
            DatabaseMngr: A DatabaseMngr instance.

        """
        if not DatabaseMngr.instance:
            engine = sqlalchemy.create_engine(
                cnfg.POSTGRES_URL,
                echo=True,
            )
            DatabaseMngr.instance = DatabaseMngr(engine)

        return typing.cast(DatabaseMngr, DatabaseMngr.instance)
