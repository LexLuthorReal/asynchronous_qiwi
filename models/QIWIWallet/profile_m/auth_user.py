import datetime
from pydantic.fields import ModelField
from typing import List, Optional, Union
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError


class IntegrationHashes(BaseModel):
    """Object: integrationHashes"""

    rostelecom: Optional[str] = Field(..., alias="rostelecom")


class IdentificationInfo(BaseModel):
    """Object: identificationInfo"""

    bank_alias: str = Field(..., alias="bankAlias")
    identification_level: str = Field(..., alias="identificationLevel")
    passport_expired: Optional[bool] = Field(..., alias="passportExpired")


class Price(BaseModel):
    """Object: price"""

    amount: float = Field(..., alias="amount")
    currency: int = Field(..., alias="currency")


class SMSNotification(BaseModel):
    """Object: identificationInfo"""

    price: Price = Field(..., alias="price")
    enabled: bool = Field(..., alias="enabled")
    active: bool = Field(..., alias="active")
    end_date: Optional[str] = Field(..., alias="endDate")


class PriorityPackage(BaseModel):
    """Object: priorityPackage"""

    price: Price = Field(..., alias="price")
    enabled: bool = Field(..., alias="enabled")
    auto_renewal_active: bool = Field(..., alias="autoRenewalActive")
    end_date: Optional[str] = Field(..., alias="endDate")


class Nickname(BaseModel):
    """Object: contractInfo"""

    nickname: Optional[str] = Field(..., alias="nickname")
    can_change: bool = Field(..., alias="canChange")
    can_use: bool = Field(..., alias="canUse")
    description: Optional[str] = Field(..., alias="description")


class PinInfo(BaseModel):
    """Object: pinInfo"""

    pin_used: bool = Field(..., alias="pinUsed")


class EmailSettings(BaseModel):
    """Object: emailSettings"""

    use_for_security: bool = Field(..., alias="use-for-security")
    use_for_promo: bool = Field(..., alias="use-for-promo")


class PassInfo(BaseModel):
    """Object: passInfo"""

    last_pass_change: Optional[Union[str, datetime.datetime]] = Field(..., alias="lastPassChange")
    next_pass_change: Optional[Union[str, datetime.datetime]] = Field(..., alias="nextPassChange")
    password_used: bool = Field(..., alias="passwordUsed")

    @validator('last_pass_change')
    def last_pass_change_datetime(cls, last_pass_change: Optional[Union[str, datetime.datetime]],
                                  field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(last_pass_change, str):
            last_pass_change = convert(value=last_pass_change, validator_name=field.name.upper())
            return last_pass_change
        elif isinstance(last_pass_change, datetime.datetime):
            return last_pass_change
        elif last_pass_change is None:
            return last_pass_change
        raise ValidationError(model=PassInfo)

    @validator('next_pass_change')
    def next_pass_change_datetime(cls, next_pass_change: Optional[Union[str, datetime.datetime]],
                                  field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(next_pass_change, str):
            next_pass_change = convert(value=next_pass_change, validator_name=field.name.upper())
            return next_pass_change
        elif isinstance(next_pass_change, datetime.datetime):
            return next_pass_change
        elif next_pass_change is None:
            return next_pass_change
        raise ValidationError(model=PassInfo)


class MobilePinInfo(BaseModel):
    """Object: mobilePinInfo"""

    last_mobile_pin_change: Optional[Union[str, datetime.datetime]] = Field(..., alias="lastMobilePinChange")
    next_mobile_pin_change: Optional[Union[str, datetime.datetime]] = Field(..., alias="nextMobilePinChange")
    mobile_pin_used: bool = Field(..., alias="mobilePinUsed")

    @validator('last_mobile_pin_change')
    def last_mobile_pin_change_datetime(cls, last_mobile_pin_change: Optional[Union[str, datetime.datetime]],
                                        field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(last_mobile_pin_change, str):
            last_mobile_pin_change = convert(value=last_mobile_pin_change, validator_name=field.name.upper())
            return last_mobile_pin_change
        elif isinstance(last_mobile_pin_change, datetime.datetime):
            return last_mobile_pin_change
        elif last_mobile_pin_change is None:
            return last_mobile_pin_change
        raise ValidationError(model=MobilePinInfo)

    @validator('next_mobile_pin_change')
    def next_mobile_pin_change_datetime(cls, next_mobile_pin_change: Optional[Union[str, datetime.datetime]],
                                        field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(next_mobile_pin_change, str):
            next_mobile_pin_change = convert(value=next_mobile_pin_change, validator_name=field.name.upper())
            return next_mobile_pin_change
        elif isinstance(next_mobile_pin_change, datetime.datetime):
            return next_mobile_pin_change
        elif next_mobile_pin_change is None:
            return next_mobile_pin_change
        raise ValidationError(model=MobilePinInfo)


class Features(BaseModel):

    feature_id: int = Field(..., alias="featureId")
    feature_value: int = Field(..., alias="featureValue")
    start_date: Union[str, datetime.datetime] = Field(..., alias="startDate")
    end_date: Union[str, datetime.datetime] = Field(..., alias="endDate")

    @validator('start_date')
    def start_date_datetime(cls, start_date: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(start_date, str):
            start_date = convert(value=start_date, validator_name=field.name.upper())
            if start_date is not None:
                return start_date
        elif isinstance(start_date, datetime.datetime):
            return start_date
        raise ValidationError(model=Features)

    @validator('end_date')
    def end_date_datetime(cls, end_date: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(end_date, str):
            end_date = convert(value=end_date, validator_name=field.name.upper())
            if end_date is not None:
                return end_date
        elif isinstance(end_date, datetime.datetime):
            return end_date
        raise ValidationError(model=Features)


class ContractInfo(BaseModel):
    """Object: contractInfo"""

    contract_id: int = Field(..., alias="contractId")
    nickname: Optional[Nickname] = Field(..., alias="nickname")
    creation_date: Union[str, datetime.datetime] = Field(..., alias="creationDate")
    features: Optional[List[Union[Features]]] = Field(..., alias="features")
    identification_info: List[IdentificationInfo] = Field(..., alias="identificationInfo")
    sms_notification: Optional[SMSNotification] = Field(..., alias="smsNotification")
    priority_package: Optional[PriorityPackage] = Field(..., alias="priorityPackage")
    blocked: bool = Field(..., alias="blocked")

    @validator('creation_date')
    def creation_date_datetime(cls, creation_date: Union[str, datetime.datetime],
                               field: ModelField) -> datetime.datetime:
        if isinstance(creation_date, str):
            creation_date = convert(value=creation_date, validator_name=field.name.upper())
            if creation_date is not None:
                return creation_date
        elif isinstance(creation_date, datetime.datetime):
            return creation_date
        raise ValidationError(model=ContractInfo)


class AuthInfo(BaseModel):
    """Object: authInfo"""

    last_login_date: Optional[str] = Field(..., alias="lastLoginDate")
    person_id: int = Field(..., alias="personId")
    registration_date: Union[str, datetime.datetime] = Field(..., alias="registrationDate")
    bound_email: Optional[str] = Field(..., alias="boundEmail")
    email_settings: Optional[EmailSettings] = Field(..., alias="emailSettings")
    mobile_pin_info: MobilePinInfo = Field(..., alias="mobilePinInfo")
    pass_info: PassInfo = Field(..., alias="passInfo")
    pin_info: PinInfo = Field(..., alias="pinInfo")
    ip: str = Field(..., alias="ip")

    @validator('registration_date')
    def registration_date_datetime(cls, registration_date: Union[str, datetime.datetime],
                                   field: ModelField) -> datetime.datetime:
        if isinstance(registration_date, str):
            registration_date = convert(value=registration_date, validator_name=field.name.upper())
            if registration_date is not None:
                return registration_date
        elif isinstance(registration_date, datetime.datetime):
            return registration_date
        raise ValidationError(model=AuthInfo)


class UserInfo(BaseModel):
    """Object: userInfo"""

    default_pay_currency: int = Field(..., alias="defaultPayCurrency")
    default_pay_account_alias: str = Field(..., alias="defaultPayAccountAlias")
    operator: str = Field(..., alias="operator")
    default_pay_source: int = Field(..., alias="defaultPaySource")
    language: str = Field(..., alias="language")
    first_txn_id: int = Field(..., alias="firstTxnId")
    phone_hash: str = Field(..., alias="phoneHash")
    integration_hashes: Optional[IntegrationHashes] = Field(..., alias="integrationHashes")


class AuthUser(BaseModel):
    """Object: AuthUser"""

    contract_info: Optional[ContractInfo] = Field(..., alias="contractInfo")
    auth_info: Optional[AuthInfo] = Field(..., alias="authInfo")
    user_info: Optional[UserInfo] = Field(..., alias="userInfo")
