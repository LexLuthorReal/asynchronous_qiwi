from loguru import logger
from pydantic.fields import ModelField
from typing import Union, List, Optional
from ....data_types.QIWIWallet import InvoicesTypes
from pydantic import BaseModel, Field, validator, ValidationError


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class ProviderData(BaseModel):

    id: int = Field(..., alias="id")
    short_name: Optional[str] = Field(..., alias="short_name")
    long_name: Optional[str] = Field(..., alias="long_name")
    logo_url: Optional[str] = Field(..., alias="logo_url")


class Bill(BaseModel):

    id: int = Field(..., alias="id")
    external_id: int = Field(..., alias="external_id")
    creation_datetime: int = Field(..., alias="creation_datetime")
    expiration_datetime: int = Field(..., alias="expiration_datetime")
    sum: AmountData = Field(..., alias="sum")
    status: Union[str, InvoicesTypes] = Field(..., alias="status")
    type: str = Field(..., alias="type")
    repetitive: bool = Field(..., alias="repetitive")
    provider: ProviderData = Field(..., alias="provider")
    comment: str = Field(..., alias="comment")
    pay_url: str = Field(..., alias="pay_url")
    from_customer: Optional[str] = Field(..., alias="from_customer")

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
        raise ValidationError(model=Bill)


class BillsData(BaseModel):

    bills: List[Union[Bill]] = Field(..., alias="bills")
    next_bill_id: Optional[int] = Field(None, alias="next_bill_id")
    next_bill_creation_datetime: Optional[int] = Field(None, alias="next_bill_creation_datetime")
