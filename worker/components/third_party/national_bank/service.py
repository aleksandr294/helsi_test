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
from components.currencies import repository as currencies_repository
import json
import datetime
from components.core import logger


cnfg = config.config


class NationalBankService:
    def __init__(
        self,
        conn: orm.Session,
        currencies_api_url: str = cnfg.BANK_URL,
        request_timeout: int = national_bank_constants.TIMEOUT,
        currencies_repo: currencies_repository.CurrenciesRepository = currencies_repository.CurrenciesRepository(),  # noqa: E501
    ):
        """
         Initializes the NationalBankService.

        Args:
            conn (orm.Session): The ORM session object for database connection.
            currencies_api_url (str, optional): The URL of the API
            to fetch currency data from.
                Defaults to cnfg.BANK_URL.
            request_timeout (int, optional): The timeout for
            the HTTP request to the API.
                Defaults to national_bank_constants.TIMEOUT.
            currencies_repo (currencies_repository.CurrenciesRepository): Repository for
            currency data. Defaults to
            currencies_repository.CurrenciesRepository().

        """
        self._currencies_api_url: str = currencies_api_url
        self._timeout: int = request_timeout

        self._currencies_repo: currencies_repository.CurrenciesRepository = (
            currencies_repo
        )
        self._conn = conn

    def get_currencies(self) -> typing.Union[str, None]:
        """
        Fetches currency data from the national bank's API.

        Returns:
            str: The JSON string containing currency data.

        """
        try:
            response = requests.get(url=self._currencies_api_url, timeout=self._timeout)
            raise requests.exceptions.Timeout
        except requests.exceptions.Timeout as ex:
            logger.app_logger.error(str(ex))
        except requests.exceptions.RequestException as ex:
            logger.app_logger.error(str(ex))
        finally:
            return response.text

    def parse_item_date(self, item: dict) -> dict:
        """
         Parses the date of a currency item.

        Args:
            item (dict): The currency item.

        Returns:
            dict: The currency item with parsed date.

        """
        date = datetime.datetime.strptime(
            item[national_bank_constants.KEY_EXCHANGEDATE],
            national_bank_constants.DATE_FORMAT,
        )
        item[national_bank_constants.KEY_EXCHANGEDATE] = date
        return item

    def parse_data(
        self, json_str: str
    ) -> typing.List[national_bank_schemas.Currencies]:
        """
         Parses the currency data from JSON string.

        Args:
            json_str (str): The JSON string containing currency data.

        Returns:
            List[national_bank_schemas.Currencies]: List of currency objects.

        """

        raw_data = json.loads(json_str)
        raw_data = list(map(self.parse_item_date, raw_data))

        type_adapter = pydantic.TypeAdapter(
            typing.List[national_bank_schemas.Currencies]
        )
        currencies_data = type_adapter.validate_python(raw_data)

        return currencies_data

    def save_currencies(self):
        """
        Fetches currency data, parses it, and saves it to the database.
        This method fetches currency data from
        the National Bank's API, parses the data into currency objects,
        and saves these objects to the database using
        the CurrenciesRepository.
        If the fetch operation fails or returns no data, the method
        will not proceed with parsing and saving.
        """
        json_str = self.get_currencies()
        if json_str:
            currencies_data = self.parse_data(json_str=json_str)
            self._currencies_repo.create_currencies(
                currencies_data=currencies_data, conn=self._conn
            )
