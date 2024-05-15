
import typing
import contextlib
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class DatabaseManager:
    def __init__(self, engine: typing.Optional[sqlalchemy.engine.Engine] = None) -> None:
        self.engine = engine

    def get_session(self) -> sessionmaker:
        """Returns session maker."""
        return sessionmaker(bind=self.engine)

    @contextlib.contextmanager
    def connect(self):
        """No docstring."""
        session_maker = self.get_session()
        with session_maker() as conn:
            yield conn

    instance: typing.Optional[typing.Any] = None

    @staticmethod
    def get():
        """Singleton method."""
        if not DatabaseManager.instance:
            engine = sqlalchemy.create_engine(
                config.get_config().postgres_url,
                echo=True,
                pool_size=10,
                max_overflow=20,
            )
            DatabaseManager.instance = DatabaseManager(engine)

        return typing.cast(DatabaseManager, DatabaseManager.instance)


def get_session(db: DatabaseManager = DatabaseManager.get()):
    """Fast API session context manager."""
    with db.connect() as conn:
        yield conn