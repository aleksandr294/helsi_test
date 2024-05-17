"""
Module defining the Currencies Pydantic model
for representing currency data.
"""

import decimal
import typing

import pydantic


class CurrencyData(pydantic.BaseModel):
    r030: int
    rate: decimal.Decimal
    cc: str
    txt: str
    currency_id: typing.Optional[int] = None
