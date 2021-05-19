from loguru import logger
import datetime
from pydantic.fields import ModelField
from typing import Union, List, Any, Optional
from ....utils.tools.str_datetime import convert
from ....data_types.QIWIWallet import InvoicesTypes
from pydantic import BaseModel, Field, validator, ValidationError


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class PayInfo(BaseModel):

    result_code: Optional[str] = Field(..., alias="resultCode")


class InvoiceData(BaseModel):

    status: Union[str, InvoicesTypes] = Field(..., alias="status")
    invoice_uid: str = Field(..., alias="invoiceUid")
    external_invoice_id: str = Field(..., alias="externalInvoiceId")
    creation_date_time: Union[str, datetime.datetime] = Field(..., alias="creationDateTime")
    change_date_time: Union[str, datetime.datetime] = Field(..., alias="changeDateTime")
    sum: AmountData = Field(..., alias="sum")
    customers: List[Any] = Field(..., alias="customers")
    extras: List[Any] = Field(..., alias="extras")
    comment: str = Field(..., alias="comment")
    payinfos: List[PayInfo] = Field(..., alias="payinfos")

    @validator('status')
    def status_types(cls, status: Union[str, InvoicesTypes], field: ModelField) -> InvoicesTypes:
        if isinstance(status, str):
            try:
                status = InvoicesTypes[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, InvoicesTypes):
            return status
        raise ValidationError(model=InvoiceData)

    @validator('creation_date_time')
    def created_date_time_datetime(cls, creation_date_time: Union[str, datetime.datetime],
                                   field: ModelField) -> datetime.datetime:
        if isinstance(creation_date_time, str):
            creation_date_time = convert(value=creation_date_time, validator_name=field.name.upper(),
                                         format_str="%Y-%m-%dT%H:%M:%S.%fZ")
            if creation_date_time is not None:
                return creation_date_time
        elif isinstance(creation_date_time, datetime.datetime):
            return creation_date_time
        raise ValidationError(model=InvoiceData)

    @validator('change_date_time')
    def change_date_time_datetime(cls, change_date_time: Union[str, datetime.datetime],
                                  field: ModelField) -> datetime.datetime:
        if isinstance(change_date_time, str):
            change_date_time = convert(value=change_date_time, validator_name=field.name.upper(),
                                       format_str="%Y-%m-%dT%H:%M:%S.%fZ")
            if change_date_time is not None:
                return change_date_time
        elif isinstance(change_date_time, datetime.datetime):
            return change_date_time
        raise ValidationError(model=InvoiceData)


class ResultData(BaseModel):

    invoices: List[Union[InvoiceData]] = Field(..., alias="invoices")
    next_invoice_date: Optional[Union[str, datetime.datetime]] = Field(..., alias="nextInvoiceDate")

    @validator('next_invoice_date')
    def change_date_time_datetime(cls, next_invoice_date: Union[str, datetime.datetime],
                                  field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(next_invoice_date, str):
            next_invoice_date = convert(value=next_invoice_date, validator_name=field.name.upper(),
                                        format_str="%Y-%m-%dT%H:%M:%S.%fZ")
            if next_invoice_date is not None:
                return next_invoice_date
        elif isinstance(next_invoice_date, datetime.datetime):
            return next_invoice_date
        elif next_invoice_date is None:
            return next_invoice_date
        raise ValidationError(model=ResultData)


class InvoicesResult(BaseModel):

    result: ResultData = Field(..., alias="result")
