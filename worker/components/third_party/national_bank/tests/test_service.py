"""
Module providing unit tests for
the NationalBankService class.
"""

import pytest
from unittest.mock import MagicMock, patch
from components.third_party.national_bank import service, schemas
from components.core.testing_database import create_sqlite_inmemory_session
from components.currencies import (
    history_currencies_repository,
    repository as currency_repository,
)
import typing
from decimal import Decimal


@pytest.fixture
def national_bank_service() -> typing.Callable:
    """
     Fixture for creating an instance of NationalBankService.

    Returns:
        Callable: A function to create an instance of
        NationalBankService with customizable parameters.

    """

    def create_national_bank_service(
        conn: MagicMock = MagicMock(),
        currencies_api_url: str = "https://example.com/api",
        timeout: int = 5,
        currency_repo: MagicMock = MagicMock(),
        history_currencies_repo: MagicMock = MagicMock(),
    ):
        return service.NationalBankService(
            conn=conn,
            currencies_api_url=currencies_api_url,
            request_timeout=timeout,
            currency_repo=currency_repo,
            history_currencies_repo=history_currencies_repo,
        )

    return create_national_bank_service


@pytest.fixture
def mock_item() -> dict:
    """
    Fixture for creating a mock currency item dictionary.

    Returns:
        dict: A mock currency item dictionary.

    """
    return dict(
        r030=36,
        txt="Австралійський долар",
        rate=26.2832,
        cc="AUD",
        exchangedate="16.05.2024",
    )


@pytest.fixture
def mock_json() -> str:
    """
     Fixture for creating a mock JSON string representing currency data.

    Returns:
        str: A mock JSON string representing currency data.

    """

    json_str = """
    [
      {
        "r030": 36,
        "txt": "Австралійський долар",
        "rate": 26.2832,
        "cc": "AUD",
        "exchangedate": "16.05.2024"
      }
    ]"""
    return json_str


@patch("requests.get")
def test_get_currencies(
    mock_request_get: MagicMock, national_bank_service: typing.Callable, mock_json: str
):
    """
    Test the retrieval of currency data from the API.

    This test function mocks the HTTP GET request
    to the currency API endpoint and
    verifies that the NationalBankService is able
    to retrieve the expected currency data.

    Args:
        mock_request_get (MagicMock): Mock object for the requests.get function.
        national_bank_service (callable): Fixture function
        for creating an instance of NationalBankService.
        mock_json (str): Mock JSON string representing currency data.

    """
    nb_service = national_bank_service()
    mock_response = MagicMock(text=mock_json)
    mock_request_get.return_value = mock_response
    result = nb_service.get_currencies()

    assert result == mock_json


def test_parse_data(national_bank_service: typing.Callable, mock_json: str):
    """
    Test the parsing of currency data from a JSON string.

    This test function verifies that the NationalBankService
    is able to parse currency data from a JSON string into
    a list of currency objects.

    Args:
        national_bank_service (callable): Fixture function for creating an
        instance of NationalBankService.
        mock_json (str): Mock JSON string representing currency data.

    """

    nb_service = national_bank_service()

    currnecies_data = [
        schemas.CurrencyData(
            r030=36,
            rate=typing.cast(Decimal, 26.2832),
            cc="AUD",
            txt="Австралійський долар",
        )
    ]

    result = nb_service.parse_data(mock_json)

    assert result == currnecies_data


@patch("requests.get")
def test_save_currencies(
    mock_request_get: MagicMock, national_bank_service: typing.Callable, mock_json: str
):
    """
    Test the saving of currency data to the database.

    This test function mocks the HTTP GET
    request to the currency API endpoint,
    retrieves currency data, saves it to the
    database using NationalBankService,
    and verifies that the data is successfully saved.

    Args:
        mock_request_get (MagicMock): Mock object for
        the requests.get function.
        national_bank_service (callable): Fixture function
        for creating an instance of NationalBankService.
        mock_json (str): Mock JSON string representing currency data.

    """
    mock_response = MagicMock(text=mock_json)
    mock_request_get.return_value = mock_response

    history_currencies_repo = (
        history_currencies_repository.HistoryCurrenciesRepository()
    )
    currency_repo = currency_repository.CurrencyRepostitory()

    with create_sqlite_inmemory_session() as conn:
        nb_service = national_bank_service(
            conn=conn,
            currency_repo=currency_repo,
            history_currencies_repo=history_currencies_repo,
        )
        nb_service.save_currencies_data()
        currencies_obj = history_currencies_repo.get_all(conn=conn)

        assert currencies_obj
