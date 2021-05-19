from loguru import logger
from typing import Optional, Union
from pydantic.fields import ModelField
from ....data_types.QIWIWallet import CardAlias, CardStatus
from pydantic import BaseModel, Field, validator, ValidationError


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class VirtualCard(BaseModel):

    id: str = Field(..., alias="id")
    card_alias: Union[str, CardAlias] = Field(..., alias="CardAlias")
    status: Union[str, CardStatus] = Field(..., alias="status")
    price: Optional[AmountData] = Field(..., alias="price")
    card_id: Optional[str] = Field(..., alias="cardId")

    @validator('card_alias')
    def card_alias_types(cls, card_alias: Union[str, CardAlias], field: ModelField) -> CardAlias:
        if isinstance(card_alias, str):
            try:
                card_alias = CardAlias(card_alias)
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return card_alias
        elif isinstance(card_alias, CardAlias):
            return card_alias
        raise ValidationError(model=VirtualCard)

    @validator('status')
    def status_types(cls, status: Union[str, CardStatus], field: ModelField) -> CardStatus:
        if isinstance(status, str):
            try:
                status = CardStatus[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, CardStatus):
            return status
        raise ValidationError(model=VirtualCard)
