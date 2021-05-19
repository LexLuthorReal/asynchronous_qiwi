import datetime
from pydantic.fields import ModelField
from typing import Optional, List, Union
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError


class Interval(BaseModel):

    date_from: Union[str, datetime.datetime] = Field(..., alias="dateFrom")
    date_till: Union[str, datetime.datetime] = Field(..., alias="dateTill")

    @validator('date_from')
    def date_from_datetime(cls, date_from: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(date_from, str):
            date_from = convert(value=date_from, validator_name=field.name.upper())
            if date_from is not None:
                return date_from
        elif isinstance(date_from, datetime.datetime):
            return date_from
        raise ValidationError(model=Interval)

    @validator('date_till')
    def date_till_datetime(cls, date_till: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(date_till, str):
            date_till = convert(value=date_till, validator_name=field.name.upper())
            if date_till is not None:
                return date_till
        elif isinstance(date_till, datetime.datetime):
            return date_till
        raise ValidationError(model=Interval)


class Limit(BaseModel):

    currency: str = Field(..., alias="currency")
    rest: float = Field(..., alias="rest")
    max: float = Field(..., alias="max")
    spent: float = Field(..., alias="spent")
    interval: Interval = Field(..., alias="interval")
    type: str = Field(..., alias="type")


class Countries(BaseModel):

    RU: List[Union[Limit]] = Field(..., alias="RU")
    KZ: List[Union[Limit]] = Field(..., alias="KZ")


class Limits(BaseModel):
    limits: Optional[Countries] = Field(..., alias="limits")
