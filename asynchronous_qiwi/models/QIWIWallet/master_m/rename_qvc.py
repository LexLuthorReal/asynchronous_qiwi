from loguru import logger
from typing import Union
from pydantic.fields import ModelField
from ....data_types.QIWIWallet import StatusesQVC
from pydantic import BaseModel, Field, validator, ValidationError


class RenameQVC(BaseModel):

    status: Union[str, StatusesQVC] = Field(..., alias="status")
    error: str = Field(..., alias="error")
    error_code: str = Field(..., alias="errorCode")

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
        raise ValidationError(model=RenameQVC)
