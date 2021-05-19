from typing import List, Union

from pydantic import BaseModel, Field


class CurrencyRate(BaseModel):
    """Model: CurrencyRate"""

    set: str = Field(..., alias="set")
    fromm: str = Field(..., alias="from")
    to: str = Field(..., alias="to")
    rate: float = Field(..., alias="rate")


class CurrencyRates(BaseModel):
    """Object: CurrencyRates"""

    result: List[Union[CurrencyRate]] = Field(..., alias="result")
