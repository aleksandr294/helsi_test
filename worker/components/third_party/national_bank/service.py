"""
Module defining the NationalBankService class for interacting with
the National Bank API and saving currency data.
"""

import typing

import pydantic
import requests
from sqlalchemy import orm
from components.core import config
from components.third_party.national_bank import (
    schemas as national_bank_schemas,
    constants as national_bank_constants,
)
from components.currencies import (
    history_currencies_repository,
    repository as currency_repository,
)
import json
from components.core import logger


cnfg = config.config


class NationalBankService:
    def __init__(
        self,
        conn: orm.Session,
        currencies_api_url: str = cnfg.BANK_URL,
        request_timeout: int = national_bank_constants.TIMEOUT,
        history_currencies_repo: history_currencies_repository.HistoryCurrenciesRepository = history_currencies_repository.HistoryCurrenciesRepository(),  # noqa: E501
        currency_repo: currency_repository.CurrencyRepostitory = currency_repository.CurrencyRepostitory(),  # noqa: E501
    ):

        self._currencies_api_url: str = currencies_api_url
        self._timeout: int = request_timeout

        self._history_currencies_repo: (
            history_currencies_repository.HistoryCurrenciesRepository
        ) = history_currencies_repo
        self._currency_repo: currency_repository.CurrencyRepostitory = currency_repo
        self._conn = conn

    def get_currencies(self) -> typing.Union[str, None]:
        """
        Fetches currency data from the national bank's API.

        Returns:
            str: The JSON string containing currency data.

        """
        try:
            response = requests.get(url=self._currencies_api_url, timeout=self._timeout)
        except requests.exceptions.Timeout as ex:
            logger.app_logger.error(str(ex))
        except requests.exceptions.RequestException as ex:
            logger.app_logger.error(str(ex))
        finally:
            return response.text

    def parse_data(
        self, json_str: str
    ) -> typing.List[national_bank_schemas.CurrencyData]:
        """
         Parses the currency data from JSON string.

        Args:
            json_str (str): The JSON string containing currency data.

        Returns:
            List[national_bank_schemas.Currencies]: List of currency objects.

        """

        raw_data = json.loads(json_str)

        type_adapter = pydantic.TypeAdapter(
            typing.List[national_bank_schemas.CurrencyData]
        )
        currencies_data = type_adapter.validate_python(raw_data)

        return currencies_data

    def save_currency(
        self, currency_data: national_bank_schemas.CurrencyData
    ) -> national_bank_schemas.CurrencyData:
        """
        Save a currency data object.

        This method saves a currency data object to the database. It first retrieves
        or creates a corresponding currency entry using the CurrencyRepository,
        then updates the currency data object with the assigned currency ID.

        Args:
            currency_data (national_bank_schemas.CurrencyData): The currency
            data object to save.

        Returns:
            national_bank_schemas.CurrencyData: The updated currency data object
            with the currency ID.

        """
        currency, is_created = self._currency_repo.get_or_create(
            currency_data=currency_data, conn=self._conn
        )
        currency_data.currency_id = currency.id  # type: ignore
        return currency_data

    def save_currencies_data(self):
        """
        Save currencies data.

        This method retrieves currencies data, parses it,
        saves each currency data object
        using the `save_currency` method, and then
        creates historical currency entries
        using the `create_currencies` method of
        the HistoryCurrenciesRepository.
        """
        json_str = self.get_currencies()
        if json_str:
            currencies_data = self.parse_data(json_str=json_str)

            currencies_data = list(map(self.save_currency, currencies_data))

            self._history_currencies_repo.create_currencies(
                currencies_data=currencies_data, conn=self._conn
            )
