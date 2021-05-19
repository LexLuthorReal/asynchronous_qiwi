import datetime
from typing import Union
from loguru import logger
from pydantic.fields import ModelField
from ....data_types.QIWIP2P import RefundTypes
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError


class AmountData(BaseModel):

    currency: str = Field(..., alias="currency")
    value: float = Field(..., alias="value")


class RefundData(BaseModel):

    amount: AmountData = Field(..., alias="amount")
    datetime_r: Union[str, datetime.datetime] = Field(..., alias="datetime")
    refund_id: str = Field(..., alias="refundId")
    status: Union[str, RefundTypes] = Field(..., alias="status")

    @validator('datetime_r')
    def datetime_r_datetime(cls, datetime_r: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(datetime_r, str):
            if datetime_r.count(":") == 3:
                datetime_r = convert(value=datetime_r, validator_name=field.name.upper())
            elif datetime_r.count(":") == 2:
                datetime_r = convert(value=datetime_r + ":00", validator_name=field.name.upper())
            if datetime_r is not None:
                return datetime_r
        elif isinstance(datetime_r, datetime.datetime):
            return datetime_r
        raise ValidationError(model=RefundData)

    @validator('status')
    def status_types(cls, status: Union[str, RefundTypes], field: ModelField) -> RefundTypes:
        if isinstance(status, str):
            try:
                status = RefundTypes[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, RefundTypes):
            return status
        raise ValidationError(model=RefundData)
