"""
Module for testing currency-related components.

This module contains fixtures and test functions to test the functionality
of currency repositories and historical currency repositories. It utilizes
fixtures to provide sample data and repository instances for testing, and
defines test functions to ensure the proper creation and retrieval of
historical currency entries.
"""

from components.currencies import repository, history_currencies_repository
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


@pytest.fixture
def history_currencies_repo() -> (
    history_currencies_repository.HistoryCurrenciesRepository
):
    """
    Fixture for providing an instance of HistoryCurrenciesRepository.

    Returns:
        history_currencies_repository.HistoryCurrenciesRepository: An instance of
        the HistoryCurrenciesRepository.

    """
    return history_currencies_repository.HistoryCurrenciesRepository()


def test_create_currencies(
    currency_data: national_bank_schemas.CurrencyData,
    currency_repo: repository.CurrencyRepostitory,
    history_currencies_repo: history_currencies_repository.HistoryCurrenciesRepository,
):
    """
    Test the creation of historical currency entries.

    This function tests the functionality of creating historical currency entries
    using the specified currency data, currency repository, and historical
    currency repository. It verifies that the creation process completes
    successfully by asserting the presence of the created historical currency
    objects.

    Args:
        currency_data (national_bank_schemas.CurrencyData): Currency data used
        for creating historical currency entries.
        currency_repo (repository.CurrencyRepostitory): Currency repository
        for fetching or creating currencies.
        history_currencies_repo: Repository for managing historical currency data.

    """
    with create_sqlite_inmemory_session() as conn:
        currency, is_created = currency_repo.get_or_create(
            currency_data=currency_data, conn=conn
        )
        currency_data.currency_id = currency.id  # type: ignore

        history_currencies_objs = history_currencies_repo.create_currencies(
            currencies_data=[currency_data], conn=conn
        )

        assert history_currencies_objs[0].id


def test_get_currencies(
    currency_data: national_bank_schemas.CurrencyData,
    currency_repo: repository.CurrencyRepostitory,
    history_currencies_repo: history_currencies_repository.HistoryCurrenciesRepository,
):
    """
      Test the retrieval of historical currency entries.

    Args:
        currency_data (national_bank_schemas.CurrencyData): Currency data
        to be used for testing.
        currency_repo (repository.CurrencyRepostitory): Currency repository for fetching
        or creating currencies.
        history_currencies_repo: Repository for
        managing historical currency data.

    """
    with create_sqlite_inmemory_session() as conn:
        currency, is_created = currency_repo.get_or_create(
            currency_data=currency_data, conn=conn
        )
        currency_data.currency_id = currency.id  # type: ignore

        history_currencies_objs = history_currencies_repo.create_currencies(
            currencies_data=[currency_data], conn=conn
        )

        history_currencies_objs = history_currencies_repo.get_all(conn=conn)
        assert history_currencies_objs
