"""
Module defining the Currencies class
representing currency data in the database.
"""

import sqlalchemy
from components.core import database


class Currency(database.Base):

    __tablename__ = "currency"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.Integer)
    text_code = sqlalchemy.Column(sqlalchemy.String(3))
    name = sqlalchemy.Column(sqlalchemy.String(100))


class HistoryCurrencies(database.Base):

    __tablename__ = "history_currencies"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    rate = sqlalchemy.Column(sqlalchemy.DECIMAL(precision=10, scale=5))  # type: ignore
    date = sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True))
    currency_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("currency.id"), nullable=True
    )
    actualy_end = sqlalchemy.Column(sqlalchemy.TIMESTAMP(timezone=True))
