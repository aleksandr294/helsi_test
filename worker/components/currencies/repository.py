"""
Module defining the CurrenciesRepository class for managing
currency data in the database.
"""

from components.currencies import models as currencies_models
import typing
from components.third_party.national_bank import schemas as national_bank_schemas
from sqlalchemy import orm
import sqlalchemy


class CurrenciesRepository:
    def __init__(
        self,
        currencies_model: type[
            currencies_models.Currencies
        ] = currencies_models.Currencies,
    ):
        """
        Initializes the CurrenciesRepository.

        Args:
            currencies_model (type[currencies_models.Currencies]): The SQLAlchemy model
             for currencies. Defaults to currencies_models.Currencies.

        """
        self._currencies_model = currencies_model

    def create_currencies(
        self,
        currencies_data: typing.List[national_bank_schemas.Currencies],
        conn: orm.Session,
    ) -> typing.List[currencies_models.Currencies]:
        """
         Creates currency objects from the provided data and saves them to the database.

        Args:
            currencies_data (List[national_bank_schemas.Currencies]): List of currency
            objects.
            conn (orm.Session): The ORM session object for database connection.

        """
        currencies_objs = [
            self._currencies_model(
                code=currency.r030,
                text_code=currency.cc,
                rate=currency.rate,
                date=currency.exchangedate,
            )
            for currency in currencies_data
        ]

        conn.add_all(currencies_objs)
        conn.commit()

        return currencies_objs

    def get_all(
        self,
        conn: orm.Session,
    ) -> typing.List[currencies_models.Currencies]:
        """
        Retrieve all currency objects from the database.

        Args:
            conn (sqlalchemy.orm.Session): An active session connected to the database.

        Returns:
            typing.List[currencies_models.Currencies]: A list of currency objects
            retrieved from the database.

        """
        query = sqlalchemy.select(currencies_models.Currencies)
        result = conn.execute(query)
        currencies_objs = list(result.scalars().all())

        return currencies_objs
