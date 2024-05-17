"""Module for fetching currencies from the database."""

from components.core import database
from components.third_party.national_bank import service


def get_currencies():
    """
    Fetch currencies from the database.

    This function retrieves currency data from
    the database using the DatabaseMngr.get_db() method,
    creates an instance of NationalBankService to interact with
    the database connection, and then
    saves the fetched currencies using the save_currencies() method
    of NationalBankService.

    """
    db = database.DatabaseMngr.get_db()
    with db.connect() as conn:
        nb_service = service.NationalBankService(conn=conn)
        nb_service.save_currencies_data()
