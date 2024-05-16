"""
Module defining the Currencies Pydantic model
for representing currency data.
"""

import datetime
import decimal

import pydantic


class Currencies(pydantic.BaseModel):
    r030: int
    rate: decimal.Decimal
    cc: str
    exchangedate: datetime.datetime
