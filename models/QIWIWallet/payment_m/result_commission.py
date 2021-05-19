from pydantic import BaseModel, Field


class AmountData(BaseModel):
    """Object: \"AmountData\""""

    amount: float = Field(..., alias="amount")
    currency: str = Field(..., alias="currency")


class ResultCommission(BaseModel):
    """Object: ResultCommission"""

    provider_id: int = Field(..., alias="providerId")
    withdraw_sum: AmountData = Field(..., alias="withdrawSum")
    enrollment_sum: AmountData = Field(..., alias="enrollmentSum")
    qw_commission: AmountData = Field(..., alias="qwCommission")
    funding_source_commission: AmountData = Field(..., alias="fundingSourceCommission")
    withdraw_to_enrollment_rate: int = Field(..., alias="withdrawToEnrollmentRate")
