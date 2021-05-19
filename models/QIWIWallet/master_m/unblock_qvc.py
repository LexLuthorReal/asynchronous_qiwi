from loguru import logger
from typing import Optional, Union
from pydantic.fields import ModelField
from ....data_types.QIWIWallet import StatusesQVC
from pydantic import BaseModel, Field, validator, ValidationError


class UnblockCardMaster(BaseModel):

    status: Union[str, StatusesQVC] = Field(..., alias="status")
    confirmation_id: Optional[str] = Field(..., alias="confirmationId")
    operation_id: Optional[str] = Field(..., alias="operationId")
    next_confirmation_request: Optional[str] = Field(..., alias="nextConfirmationRequest")

    @validator('status')
    def status_types(cls, status: Union[str, StatusesQVC], field: ModelField) -> StatusesQVC:
        if isinstance(status, str):
            try:
                status = StatusesQVC[status]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return status
        elif isinstance(status, StatusesQVC):
            return status
        raise ValidationError(model=UnblockCardMaster)
