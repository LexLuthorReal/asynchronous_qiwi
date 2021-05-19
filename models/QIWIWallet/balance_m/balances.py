from typing import List, Optional, Union

from pydantic import BaseModel, Field


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Type(BaseModel):
    """Object: type"""

    id: str = Field(..., alias="id")
    title: str = Field(..., alias="title")


class Accounts(BaseModel):
    """Object: accounts"""

    alias: str = Field(..., alias="alias")
    fs_alias: str = Field(..., alias="fsAlias")
    bank_alias: str = Field(..., alias="bankAlias")
    title: str = Field(..., alias="title")
    type: Type = Field(..., alias="type")
    has_balance: bool = Field(..., alias="hasBalance")
    balance: Optional[AmountData] = Field(..., alias="balance")
    currency: int = Field(..., alias="currency")
    default_account: bool = Field(..., alias="defaultAccount")


class AvailableType(BaseModel):
    """Object: available_type"""

    alias: str = Field(..., alias="alias")
    currency: int = Field(..., alias="currency")


class AvailableBalances(BaseModel):
    """Object AvailableBalances"""

    available_balances: Optional[List[Union[AvailableType]]] = Field(...)


class ListBalances(BaseModel):
    """Object: Balance"""

    accounts: List[Accounts] = Field(..., alias="accounts")
