import datetime
from typing import Union
from pydantic.fields import ModelField
from ....utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError


class TokenDetails(BaseModel):

    name: str = Field(..., alias="name")
    public_key: str = Field(..., alias="publicKey")
    secret_key: str = Field(..., alias="secretKey")
    created_date_time: Union[str, datetime.datetime] = Field(..., alias="createdDateTime")

    @validator('created_date_time')
    def created_date_time_datetime(cls, created_date_time: Union[str, datetime.datetime],
                                   field: ModelField) -> datetime.datetime:
        if isinstance(created_date_time, str):
            created_date_time = convert(value=created_date_time, validator_name=field.name.upper(),
                                        format_str="%Y-%m-%dT%H:%M:%S.%fZ")
            if created_date_time is not None:
                return created_date_time
        elif isinstance(created_date_time, datetime.datetime):
            return created_date_time
        raise ValidationError(model=TokenDetails)


class TokenResult(BaseModel):

    result: TokenDetails = Field(..., alias="result")
