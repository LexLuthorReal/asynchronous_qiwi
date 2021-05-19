from loguru import logger
import datetime
from pydantic.fields import ModelField
from typing import Optional, List, Union, Any
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError
from ....data_types.QIWIWallet.list_qvc import ReleasedCardStatus, CardType, CardAlias


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Requisites(BaseModel):
    name: str = Field(..., alias="name")
    value: str = Field(..., alias="value")


class Details(BaseModel):
    info: str = Field(..., alias="info")
    description: str = Field(..., alias="description")
    tariff_link: str = Field(..., alias="tariffLink")
    offer_link: str = Field(..., alias="offerLink")
    features: List[Any] = Field(..., alias="features")
    requisites: List[Union[Requisites]] = Field(..., alias="requisites")


class Info(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    alias: Union[str, CardAlias] = Field(..., alias="alias")
    price: AmountData = Field(..., alias="price")
    period: str = Field(..., alias="period")
    type: Union[str, CardAlias] = Field(..., alias="type")
    details: Details = Field(..., alias="details")

    @validator("alias")
    def alias_type(cls, alias: Union[str, CardAlias], field: ModelField) -> CardAlias:
        if isinstance(alias, str):
            try:
                alias = CardAlias(alias)
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return alias
        elif isinstance(alias, CardAlias):
            return alias
        raise ValidationError(model=Info)

    @validator("type")
    def card_type_type(cls, card_type: Union[str, CardAlias], field: ModelField) -> CardAlias:
        if isinstance(card_type, str):
            try:
                card_type = CardAlias[card_type]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return card_type
        elif isinstance(card_type, CardAlias):
            return card_type
        raise ValidationError(model=Info)


class QVX(BaseModel):
    id: int = Field(..., alias="id")
    masked_pan: str = Field(..., alias="maskedPan")
    status: Optional[Union[str, ReleasedCardStatus]] = Field(..., alias="status")
    card_expire: Optional[Union[str, datetime.datetime]] = Field(..., alias="cardExpire")
    card_type: Optional[Union[str, CardType]] = Field(..., alias="cardType")
    card_alias: str = Field(..., alias="cardAlias")
    card_limit: Optional[str] = Field(..., alias="cardLimit")
    activated: Optional[Union[str, datetime.datetime]] = Field(..., alias="activated")
    sms_resended: Optional[Union[str, datetime.datetime]] = Field(..., alias="smsResended")
    post_number: Optional[str] = Field(..., alias="postNumber")
    blocked_date: Optional[Union[str, datetime.datetime]] = Field(..., alias="blockedDate")
    full_pan: Optional[str] = Field(..., alias="fullPan")
    card_id: int = Field(..., alias="cardId")
    txn_id: str = Field(..., alias="txnId")
    card_expire_month: str = Field(..., alias="cardExpireMonth")
    card_expire_year: str = Field(..., alias="cardExpireYear")

    @validator('status')
    def status_types(cls, status: Union[str, ReleasedCardStatus], field: ModelField) -> ReleasedCardStatus:
        if isinstance(status, str):
            try:
                status = ReleasedCardStatus[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, ReleasedCardStatus):
            return status
        raise ValidationError(model=QVX)

    @validator('card_expire')
    def card_expire_datetime(cls, card_expire: Optional[Union[str, datetime.datetime]],
                             field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(card_expire, str):
            card_expire = convert(value=card_expire, validator_name=field.name.upper(), alert=False)
            return card_expire
        elif isinstance(card_expire, datetime.datetime):
            return card_expire
        elif card_expire is None:
            return card_expire
        raise ValidationError(model=QVX)

    @validator('card_type')
    def card_types(cls, card_type: Union[str, CardType], field: ModelField) -> CardType:
        if isinstance(card_type, str):
            try:
                card_type = CardType[card_type]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return card_type
        elif isinstance(card_type, CardType):
            return card_type
        raise ValidationError(model=QVX)

    @validator('activated')
    def activated_datetime(cls, activated: Optional[Union[str, datetime.datetime]],
                           field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(activated, str):
            activated = convert(value=activated, validator_name=field.name.upper(), alert=False)
            return activated
        elif isinstance(activated, datetime.datetime):
            return activated
        elif activated is None:
            return activated
        raise ValidationError(model=QVX)

    @validator('sms_resended')
    def sms_resended_datetime(cls, sms_resended: Optional[Union[str, datetime.datetime]],
                              field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(sms_resended, str):
            sms_resended = convert(value=sms_resended, validator_name=field.name.upper(), alert=False)
            return sms_resended
        elif isinstance(sms_resended, datetime.datetime):
            return sms_resended
        elif sms_resended is None:
            return sms_resended
        raise ValidationError(model=QVX)

    @validator('blocked_date')
    def blocked_date_datetime(cls, blocked_date: Optional[Union[str, datetime.datetime]],
                              field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(blocked_date, str):
            blocked_date = convert(value=blocked_date, validator_name=field.name.upper(), alert=False)
            return blocked_date
        elif isinstance(blocked_date, datetime.datetime):
            return blocked_date
        elif blocked_date is None:
            return blocked_date
        raise ValidationError(model=QVX)


class ListCard(BaseModel):
    qvx: QVX = Field(..., alias="qvx")
    balance: Optional[AmountData] = Field(..., alias="balance")
    info: Info = Field(..., alias="info")
    features: List[Any] = Field(..., alias="features")


class ListCardMaster(BaseModel):
    data: List[Union[ListCard]] = Field(..., alias="data")
