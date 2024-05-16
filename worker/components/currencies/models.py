"""
Module defining the Currencies class
representing currency data in the database.
"""

import sqlalchemy
from components.core import database


class Currencies(database.Base):

    __tablename__ = "currencies"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.Integer)
    text_code = sqlalchemy.Column(sqlalchemy.String(3))
    rate = sqlalchemy.Column(sqlalchemy.DECIMAL(precision=10, scale=5))  # type: ignore
    date = sqlalchemy.Column(sqlalchemy.Date)
