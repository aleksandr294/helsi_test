"""
Module for managing currency data using a repository 
pattern and testing with pytest.

This module defines the CurrencyRepository class, 
which provides methods to interact with currency data.
It also includes fixtures and tests to verify 
the functionality of this repository, particularly the
get_or_create method. The tests use an in-memory 
SQLite database for isolated and repeatable test runs.

"""

from components.currencies import models as currency_models
import typing
from components.third_party.national_bank import schemas as national_bank_schemas
from sqlalchemy import orm
import sqlalchemy


class CurrencyRepostitory:
    def __init__(
        self,
        currency_model: type[currency_models.Currency] = currency_models.Currency,
    ):

        self._currency_model = currency_model

    def get_or_create(
        self,
        currency_data: national_bank_schemas.CurrencyData,
        conn: orm.Session,
    ) -> typing.Tuple[currency_models.Currency, bool]:
        """
        Retrieve a currency object if it exists, otherwise create it.

        Args:
            currency_data (national_bank_schemas.CurrencyData): The data for
            the currency to get or create.
            conn (orm.Session): The database session to use for the query.

        Returns:
            typing.Tuple[currency_models.Currency, bool]: A tuple containing
            the currency object and a boolean
            indicating whether the object was created (True) or already
            existed (False).

        """
        query = sqlalchemy.select(self._currency_model).where(
            self._currency_model.code == currency_data.r030
        )
        result = conn.execute(query)
        currency = result.scalar()
        if currency:
            return currency, False
        else:

            currency = self._currency_model(
                code=currency_data.r030,
                text_code=currency_data.cc,
                name=currency_data.txt,
            )

            conn.add(currency)
            conn.commit()
            return currency, True
