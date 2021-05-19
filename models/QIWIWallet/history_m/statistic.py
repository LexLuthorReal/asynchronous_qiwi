from typing import List
from pydantic import BaseModel, Field


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Statistic(BaseModel):
    """Object: Stats"""

    incoming_total: List[AmountData] = Field(..., alias="incomingTotal")
    outgoing_total: List[AmountData] = Field(..., alias="outgoingTotal")
