from loguru import logger
from typing import Union
from pydantic.fields import ModelField
from ....data_types.QIWIWallet import HookType, NotifyType
from pydantic import BaseModel, Field, validator, ValidationError


class HookURL(BaseModel):

    url: str = Field(..., alias="url")


class HookData(BaseModel):

    hook_id: str = Field(..., alias="hookId")
    hook_parameters: HookURL = Field(..., alias="hookParameters")
    hook_type: Union[str, HookType] = Field(..., alias="hookType")
    txn_type: Union[str, NotifyType] = Field(..., alias="txnType")

    @validator('hook_type')
    def hook_type_types(cls, hook_type: Union[str, HookType], field: ModelField) -> HookType:
        if isinstance(hook_type, str):
            try:
                hook_type = HookType[hook_type]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return hook_type
        elif isinstance(hook_type, HookType):
            return hook_type
        raise ValidationError(model=HookData)

    @validator('txn_type')
    def txn_type_types(cls, txn_type: Union[str, HookType], field: ModelField) -> NotifyType:
        if isinstance(txn_type, str):
            try:
                txn_type = NotifyType[txn_type]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return txn_type
        elif isinstance(txn_type, NotifyType):
            return txn_type
        raise ValidationError(model=HookData)
