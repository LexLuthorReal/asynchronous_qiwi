from typing import Optional, TypeVar, Union

from pydantic import BaseModel, Field

P = TypeVar("P")


class AmountData(BaseModel):
    """Object: sum"""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class PaymentMethod(BaseModel):
    """Object: paymentMethod"""

    type: str = Field(..., alias="type")
    account_id: str = Field(..., alias="accountId")


class QIWIMasterFields(BaseModel):
    """Object: fields"""

    account: str = Field(..., alias="account")
    vas_alias: str = Field(..., alias="vas_alias")


class BuyVirtualCardFields(BaseModel):

    account: str = Field(..., alias="account")
    order_id: str = Field(..., alias="order_id")


class AccountField(BaseModel):

    account: str = Field(..., alias="account")


class CardFields(AccountField):

    rec_address: str = Field(..., alias="rec_address")
    rec_city: str = Field(..., alias="rec_city")
    rec_country: str = Field(..., alias="rec_country")
    reg_name: str = Field(..., alias="reg_name")
    reg_name_f: str = Field(..., alias="reg_name_f")
    rem_name: str = Field(..., alias="rem_name")
    rem_name_f: str = Field(..., alias="rem_name_f")


class FreeDetails(BaseModel):

    extra_to_bik: str = Field(..., alias="extra_to_bik")
    request_protocol: str = Field(..., alias="requestProtocol")
    city: str = Field(..., alias="city")
    name: str = Field(..., alias="name")
    to_bik: str = Field(..., alias="to_bik")
    urgent: str = Field(..., alias="urgent")
    to_kpp: str = Field(..., alias="to_kpp")
    is_commercial: str = Field(..., alias="is_commercial")
    nds: str = Field(..., alias="nds")
    goal: str = Field(..., alias="goal")
    from_name_p: str = Field(..., alias="from_name_p")
    from_name: str = Field(..., alias="from_name")
    from_name_f: str = Field(..., alias="from_name_f")
    info: str = Field(..., alias="info")
    to_name: str = Field(..., alias="to_name")
    to_inn: str = Field(..., alias="to_inn")
    account: str = Field(..., alias="account")
    to_service_id: str = Field(..., alias="toServiceId")


class Payment(BaseModel):
    """Object: Payment"""

    id: str = Field(..., alias="id")
    sum: AmountData = Field(..., alias="sum")
    payment_method: PaymentMethod = Field(..., alias="paymentMethod")
    comment: Optional[str] = Field(..., alias="comment")
    fields: Union[QIWIMasterFields,
                  BuyVirtualCardFields,
                  AccountField,
                  CardFields,
                  FreeDetails] = Field(..., alias="fields")


class State(BaseModel):
    """Object: state"""

    code: str = Field(..., alias="code")


class PurchaseTotals(BaseModel):
    """Object: paymentMethod"""

    total: AmountData = Field(..., alias="total")


class Commission(AccountField):

    payment_method: PaymentMethod = Field(..., alias="paymentMethod")
    purchase_totals: PurchaseTotals = Field(..., alias="purchaseTotals")


class Transaction(BaseModel):
    """Object: transaction"""

    id: str = Field(..., alias="id")
    state: State = Field(..., alias="state")


class PaymentInfo(BaseModel):

    id: str = Field(..., alias="id")
    terms: str = Field(..., alias="terms")
    fields: AccountField = Field(..., alias="fields")
    sum: AmountData = Field(..., alias="sum")
    transaction: Transaction = Field(..., alias="transaction")
    comment: Optional[str] = Field(None, alias="comment")
    source: Optional[str] = Field(..., alias="source")
