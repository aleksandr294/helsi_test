"""
Module providing functionality for
testing currency creation in the database.
"""

from components.currencies import repository
from components.core.testing_database import create_sqlite_inmemory_session
from components.third_party.national_bank import schemas as national_bank_schemas
import datetime


def test_create_currencies():
    """
    Test the creation of currency objects in the database.

    This test function creates a `CurrenciesRepository`
    object and attempts to create
    currency objects in the database using a sample currency data.
    It then verifies
    that the creation was successful by checking if any currency
    objects were returned.

    Raises:
        AssertionError: If no currency objects are created or returned.

    """
    currencies_repo = repository.CurrenciesRepository()
    currencies = [
        national_bank_schemas.Currencies(
            r030=36,
            txt="Австралійський долар",
            rate=26.2832,
            cc="AUD",
            exchangedate=datetime.datetime(year=2024, month=5, day=16),
        )
    ]

    with create_sqlite_inmemory_session() as conn:
        currencies_objs = currencies_repo.create_currencies(
            currencies_data=currencies, conn=conn
        )

        assert currencies_objs
