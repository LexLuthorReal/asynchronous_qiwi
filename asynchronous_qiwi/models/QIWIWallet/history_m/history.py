from loguru import logger
import datetime
from pydantic.fields import ModelField
from typing import Any, List, Optional, Union
from ....utils.tools.str_datetime import convert
from ....data_types.error_codes.qiwi_errors import QIWIErrorsID
from pydantic import BaseModel, Field, validator, ValidationError
from ....data_types.QIWIWallet import PaymentTypes, PaymentStatuses


class NextPayment(BaseModel):
    """
    Object: NextPayment this is start point for next payment
    Use previous Payment object for get&set this data for get new payments if you need
    Or you can use all_transaction argument for get all payments
    """

    next_txn_date: Union[datetime.datetime] = Field(..., alias="nextTxnDate")
    next_txn_id: int = Field(..., alias="nextTxnId")


class Extras(BaseModel):
    """Object: extras"""

    key: Optional[str] = Field(..., alias="key")
    value: Optional[str] = Field(..., alias="value")


class ProviderAndSource(BaseModel):
    """Object: provider"""

    id: int = Field(..., alias="id")
    short_name: str = Field(..., alias="shortName")
    long_name: Optional[str] = Field(..., alias="longName")
    logo_url: Optional[str] = Field(..., alias="logoUrl")
    description: Optional[str] = Field(..., alias="description")
    keys: Optional[str] = Field(..., alias="keys")
    site_url: Optional[str] = Field(..., alias="siteUrl")
    extras: Optional[List[Union[Extras]]] = Field(..., alias="extras")


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class Features(BaseModel):
    """Object: features"""

    cheque_ready: bool = Field(..., alias="chequeReady")
    bank_document_ready: bool = Field(..., alias="bankDocumentReady")
    regular_payment_enabled: bool = Field(..., alias="regularPaymentEnabled")
    bank_document_available: bool = Field(..., alias="bankDocumentAvailable")
    repeat_payment_enabled: bool = Field(..., alias="repeatPaymentEnabled")
    favorite_payment_enabled: bool = Field(..., alias="favoritePaymentEnabled")
    chat_available: bool = Field(..., alias="chatAvailable")
    greeting_card_attached: bool = Field(..., alias="greetingCardAttached")


class View(BaseModel):
    """Object: view"""

    title: str = Field(..., alias="title")
    account: str = Field(..., alias="title")


class PaymentData(BaseModel):
    """Object: data"""

    txn_id: int = Field(..., alias="txnId")
    person_id: int = Field(..., alias="personId")
    date: Union[str, datetime.datetime] = Field(..., alias="date")
    error_code: int = Field(..., alias="errorCode")
    error: Optional[str] = Field(..., alias="error")
    status: Union[str, PaymentStatuses] = Field(..., alias="status")
    type: Optional[Union[str, PaymentTypes]] = Field(..., alias="type")
    status_text: str = Field(..., alias="statusText")
    trm_txn_id: str = Field(..., alias="trmTxnId")
    account: str = Field(..., alias="account")
    sum: AmountData = Field(..., alias="sum")
    commission: AmountData = Field(..., alias="commission")
    total: AmountData = Field(..., alias="total")
    provider: ProviderAndSource = Field(..., alias="provider")
    source: ProviderAndSource = Field(..., alias="source")
    comment: Optional[str] = Field(..., alias="comment")
    currency_rate: int = Field(..., alias="currencyRate")
    payment_extras: List[Any] = Field(..., alias="paymentExtras")
    features: Features = Field(..., alias="features")
    service_extras: Optional[Any] = Field(..., alias="serviceExtras")
    view: View = Field(..., alias="view")

    @validator('date')
    def date_datetime(cls, date: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(date, str):
            date = convert(value=date, validator_name=field.name.upper())
            if date is not None:
                return date
        elif isinstance(date, datetime.datetime):
            return date
        raise ValidationError(model=PaymentData)

    @validator('error')
    def error_types(cls, error: Optional[str], values: dict, field: ModelField) -> Optional[str]:
        error_code = values["error_code"]
        if isinstance(error_code, int):
            try:
                error = QIWIErrorsID[error_code]
            except KeyError as e:
                logger.warning(f"[VALIDATION ERROR_CODE NOT EXIST] {field.name.upper()}: " + str(e))
            else:
                return error
        elif error_code is None:
            return error
        raise ValidationError(model=PaymentData)

    @validator('status')
    def status_types(cls, status: Union[str, PaymentStatuses], field: ModelField) -> PaymentStatuses:
        if isinstance(status, str):
            try:
                status = PaymentStatuses[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, PaymentStatuses):
            return status
        raise ValidationError(model=PaymentData)

    @validator('type')
    def type_types(cls, type_operation: Union[str, PaymentTypes], field: ModelField) -> PaymentTypes:
        if isinstance(type_operation, str):
            try:
                type_operation = PaymentTypes[type_operation]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return type_operation
        elif isinstance(type_operation, PaymentTypes):
            return type_operation
        raise ValidationError(model=PaymentData)


class History(BaseModel):
    """Object: History"""

    data: List[PaymentData] = Field(..., alias="data")
    next_txn_id: Optional[int] = Field(..., alias="nextTxnId")
    next_txn_date: Optional[Union[str, datetime.datetime]] = Field(..., alias="nextTxnDate")

    @validator('next_txn_date')
    def date_datetime(cls, next_txn_date: Optional[Union[str, datetime.datetime]],
                      field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(next_txn_date, str):
            try:
                next_txn_date = datetime.datetime.strptime(next_txn_date, "%Y-%m-%dT%H:%M:%S%z")
            except ValueError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return next_txn_date
        elif isinstance(next_txn_date, datetime.datetime):
            return next_txn_date
        elif next_txn_date is None:
            return next_txn_date
        raise ValidationError(model=History)
