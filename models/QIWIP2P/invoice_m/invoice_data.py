import datetime
from loguru import logger
from pydantic.fields import ModelField
from typing import Optional, Union, Dict, Any
from ....utils.tools.str_datetime import convert
from ....data_types.QIWIWallet import InvoicesTypes
from pydantic import BaseModel, Field, validator, ValidationError


class StandardCustomFields(BaseModel):

    pay_sources_filter: str = Field(..., alias="paySourcesFilter")
    theme_code: str = Field(..., alias="themeCode")


class CustomerData(BaseModel):

    phone: Optional[str] = Field(None, alias="phone")
    email: Optional[str] = Field(None, alias="email")
    account: Optional[str] = Field(None, alias="account")


class StatusInfo(BaseModel):

    value: str = Field(..., alias="value")
    changed_date_time: Union[str, datetime.datetime] = Field(..., alias="changedDateTime")

    @validator('value')
    def value_types(cls, value: Union[str, InvoicesTypes], field: ModelField) -> InvoicesTypes:
        if isinstance(value, str):
            try:
                value = InvoicesTypes[value]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return value
        elif isinstance(value, InvoicesTypes):
            return value
        raise ValidationError(model=StatusInfo)

    @validator('changed_date_time')
    def changed_date_time_datetime(cls, changed_date_time: Union[str, datetime.datetime],
                                   field: ModelField) -> datetime.datetime:
        if isinstance(changed_date_time, str):
            if "." in changed_date_time:
                changed_date_time = convert(value=changed_date_time, validator_name=field.name.upper(),
                                            format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                changed_date_time = convert(value=changed_date_time, validator_name=field.name.upper())
            if changed_date_time is not None:
                return changed_date_time
        elif isinstance(changed_date_time, datetime.datetime):
            return changed_date_time
        raise ValidationError(model=StatusInfo)


class AmountData(BaseModel):

    currency: str = Field(..., alias="currency")
    value: float = Field(..., alias="value")


class Invoice(BaseModel):

    site_id: str = Field(..., alias="siteId")
    bill_id: str = Field(..., alias="billId")
    amount: AmountData = Field(..., alias="amount")
    status: StatusInfo = Field(..., alias="status")
    custom_fields: Optional[Union[StandardCustomFields, Dict[str, Any]]] = Field(None, alias="customFields")
    customer: Optional[CustomerData] = Field(None, alias="customer")
    comment: Optional[str] = Field(None, alias="comment")
    creation_date_time: Union[str, datetime.datetime] = Field(..., alias="creationDateTime")
    expiration_date_time: Union[str, datetime.datetime] = Field(..., alias="expirationDateTime")
    payUrl: str = Field(..., alias="payUrl")

    @validator('creation_date_time')
    def creation_date_time_datetime(cls, creation_date_time: Union[str, datetime.datetime],
                                    field: ModelField) -> datetime.datetime:
        if isinstance(creation_date_time, str):
            if "." in creation_date_time:
                creation_date_time = convert(value=creation_date_time, validator_name=field.name.upper(),
                                             format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                creation_date_time = convert(value=creation_date_time, validator_name=field.name.upper())
            if creation_date_time is not None:
                return creation_date_time
        elif isinstance(creation_date_time, datetime.datetime):
            return creation_date_time
        raise ValidationError(model=Invoice)

    @validator('expiration_date_time')
    def expiration_date_time_datetime(cls, expiration_date_time: Union[str, datetime.datetime],
                                      field: ModelField) -> datetime.datetime:
        if isinstance(expiration_date_time, str):
            if "." in expiration_date_time:
                expiration_date_time = convert(value=expiration_date_time, validator_name=field.name.upper(),
                                               format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                expiration_date_time = convert(value=expiration_date_time, validator_name=field.name.upper())
            if expiration_date_time is not None:
                return expiration_date_time
        elif isinstance(expiration_date_time, datetime.datetime):
            return expiration_date_time
        raise ValidationError(model=Invoice)


class CreateInvoice(BaseModel):

    amount: AmountData = Field(..., alias="amount")
    expiration_date_time: str = Field(..., alias="expirationDateTime")
    customer: Optional[CustomerData] = Field(None, alias="customer")
    comment: Optional[str] = Field(None, alias="comment")
    custom_fields: Optional[Union[StandardCustomFields, Dict[str, Any]]] = Field(None, alias="customFields")
