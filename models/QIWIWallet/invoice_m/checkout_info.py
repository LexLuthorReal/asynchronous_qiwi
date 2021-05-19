import datetime
from loguru import logger
from pydantic.fields import ModelField
from typing import Optional, Union, List
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError
from ....data_types.QIWIWallet import PayMethodFilter, InvoicesTypes


class AmountData(BaseModel):

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class CheckoutInvoiceInfo(BaseModel):

    invoice_uid: str = Field(..., alias="invoiceUid")
    invoice_status: Union[str, InvoicesTypes] = Field(..., alias="invoiceStatus")
    amount: AmountData = Field(..., alias="amount")
    create_date_time: Union[str, datetime.datetime] = Field(..., alias="createDateTime")
    expire_date_time: Union[str, datetime.datetime] = Field(..., alias="expireDateTime")
    merchant_id: str = Field(..., alias="merchantId")
    invoice_ext_id: str = Field(..., alias="invoiceExtId")
    comment: Optional[str] = Field(..., alias="comment")
    pay_methods_filter: Union[List[str], List[PayMethodFilter]] = Field(..., alias="payMethodsFilter")

    @validator('invoice_status')
    def invoice_status_types(cls, invoice_status: Union[str, InvoicesTypes], field: ModelField) -> InvoicesTypes:
        if isinstance(invoice_status, str):
            try:
                invoice_status = InvoicesTypes[invoice_status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return invoice_status
        elif isinstance(invoice_status, InvoicesTypes):
            return invoice_status
        raise ValidationError(model=CheckoutInvoiceInfo)

    @validator('create_date_time')
    def create_date_time_datetime(cls, create_date_time: Union[str, datetime.datetime],
                                  field: ModelField) -> datetime.datetime:
        if isinstance(create_date_time, str):
            if "." in create_date_time:
                create_date_time = convert(value=create_date_time, validator_name=field.name.upper(),
                                           format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                create_date_time = convert(value=create_date_time, validator_name=field.name.upper())
            if create_date_time is not None:
                return create_date_time
        elif isinstance(create_date_time, datetime.datetime):
            return create_date_time
        raise ValidationError(model=CheckoutInvoiceInfo)

    @validator('expire_date_time')
    def expire_date_time_datetime(cls, expire_date_time: Union[str, datetime.datetime],
                                  field: ModelField) -> datetime.datetime:
        if isinstance(expire_date_time, str):
            if "." in expire_date_time:
                expire_date_time = convert(value=expire_date_time, validator_name=field.name.upper(),
                                           format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                expire_date_time = convert(value=expire_date_time, validator_name=field.name.upper())
            if expire_date_time is not None:
                return expire_date_time
        elif isinstance(expire_date_time, datetime.datetime):
            return expire_date_time
        raise ValidationError(model=CheckoutInvoiceInfo)

    @validator('pay_methods_filter')
    def pay_methods_filter_types(cls, pay_methods_filter: Union[List[str], List[PayMethodFilter]],
                                 field: ModelField) -> List[PayMethodFilter]:
        if isinstance(pay_methods_filter, List):
            try:
                pay_methods_filter = [PayMethodFilter[v] for v in pay_methods_filter]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return pay_methods_filter
        if isinstance(pay_methods_filter[0], PayMethodFilter):
            return pay_methods_filter
        raise ValidationError(model=CheckoutInvoiceInfo)
