"""
Module for testing the currency repository
functionality using pytest fixtures.
This module includes fixtures and tests to verify the behavior
of the CurrencyRepository,
particularly the get_or_create method. The tests use an
in-memory SQLite database for
isolated and repeatable test runs.
"""

from components.currencies import repository
from components.core.testing_database import create_sqlite_inmemory_session
from components.third_party.national_bank import schemas as national_bank_schemas
import pytest
from decimal import Decimal


@pytest.fixture
def currency_data() -> national_bank_schemas.CurrencyData:
    """
    Fixture that provides a CurrencyData object for testing.

    Returns:
        national_bank_schemas.CurrencyData: A CurrencyData object
        with sample data.

    """
    return national_bank_schemas.CurrencyData(
        r030=36,
        txt="Австралійський долар",
        rate=Decimal(26.2832),
        cc="AUD",
    )


@pytest.fixture
def currency_repo() -> repository.CurrencyRepostitory:
    """
    Fixture that provides a CurrencyRepository object for testing.

    Returns:
        repository.CurrencyRepostitory: An instance of CurrencyRepostitory.

    """
    return repository.CurrencyRepostitory()


def test_get_or_create_currencies(
    currency_data: national_bank_schemas.CurrencyData,
    currency_repo: repository.CurrencyRepostitory,
):
    """
    Test for the get_or_create method of CurrencyRepository.

    Args:
        currency_data (national_bank_schemas.CurrencyData): The currency data
        to test with.
        currency_repo (repository.CurrencyRepostitory): The currency repository
        to test with.

    Asserts:
        bool: The currency object is created and returned successfully.
        bool: The currency object is not created again if it already exists.

    """
    with create_sqlite_inmemory_session() as conn:
        currencies_objs, is_created = currency_repo.get_or_create(
            currency_data=currency_data, conn=conn
        )

        assert currencies_objs and is_created

        currencies_objs, is_created = currency_repo.get_or_create(
            currency_data=currency_data, conn=conn
        )
        assert currencies_objs and not is_created
