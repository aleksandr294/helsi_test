"""
Module for managing historical currency data.

This module contains the `HistoryCurrenciesRepository` class, which provides
functionality for creating and retrieving historical currency entries in the database.
It utilizes SQLAlchemy for database interactions and defines methods for creating
new historical currency entries and retrieving all existing entries.
"""

import datetime

from components.currencies import models as currency_models, constants
import typing
from components.third_party.national_bank import schemas as national_bank_schemas
from sqlalchemy import orm
import sqlalchemy


class HistoryCurrenciesRepository:
    def __init__(
        self,
        history_currencies_models: type[
            currency_models.HistoryCurrencies
        ] = currency_models.HistoryCurrencies,
    ):

        self._history_currencies_model = history_currencies_models

    def create_currencies(
        self,
        currencies_data: typing.List[national_bank_schemas.CurrencyData],
        conn: orm.Session,
    ) -> typing.List[currency_models.HistoryCurrencies]:
        """
        Create historical currency entries in the database.

        Args:
            currencies_data (typing.List[national_bank_schemas.CurrencyData]): List of
            currency data to create.
            conn (orm.Session): Database connection.

        Returns:
            typing.List[currency_models.HistoryCurrencies]: List of created historical
            currency objects.

        """
        dt_utc = datetime.datetime.utcnow()

        currencies_objs = [
            self._history_currencies_model(
                currency_id=currency_data.currency_id,
                rate=currency_data.rate,
                date=dt_utc,
                actualy_end=dt_utc + datetime.timedelta(minutes=constants.MINUTE),
            )
            for currency_data in currencies_data
        ]

        conn.add_all(currencies_objs)
        conn.commit()

        return currencies_objs

    def get_all(
        self,
        conn: orm.Session,
    ) -> typing.List[currency_models.HistoryCurrencies]:
        """
        Retrieve all historical currency entries from the database.

        Args:
            conn (orm.Session): Database connection.

        Returns:
            typing.List[currency_models.HistoryCurrencies]: List of all
            historical currency objects.

        """
        query = sqlalchemy.select(self._history_currencies_model)
        result = conn.execute(query)
        currencies_objs = list(result.scalars().all())

        return currencies_objs
