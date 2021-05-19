from typing import Any
from pydantic import BaseModel, Field


class BillPayment(BaseModel):

    invoice_status: str = Field(..., alias="invoice_status")
    is_sms_confirm: bool = Field(..., alias="is_sms_confirm")
    WALLET_ACCEPT_PAY_RESULT: Any = Field(..., alias="WALLET_ACCEPT_PAY_RESULT")
