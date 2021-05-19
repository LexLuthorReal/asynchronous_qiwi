import datetime
from typing import Union
from pydantic.fields import ModelField
from ..utils.tools.str_datetime import convert
from pydantic import BaseModel, Field, validator, ValidationError


class SomeError(BaseModel):

    service_name: str = Field(..., alias="serviceName")
    error_code: str = Field(..., alias="errorCode")
    description: str = Field(..., alias="description")
    user_message: str = Field(..., alias="userMessage")
    date_time: Union[str, datetime.datetime] = Field(..., alias="dateTime")
    trace_id: str = Field(..., alias="traceId")

    @validator('date_time')
    def date_time_datetime(cls, date_time: Union[str, datetime.datetime], field: ModelField) -> datetime.datetime:
        if isinstance(date_time, str):
            if "." in date_time:
                date_time = convert(value=date_time, validator_name=field.name.upper(),
                                    format_str="%Y-%m-%dT%H:%M:%S.%f%z")
            else:
                date_time = convert(value=date_time, validator_name=field.name.upper())
            if date_time is not None:
                return date_time
        elif isinstance(date_time, datetime.datetime):
            return date_time
        raise ValidationError(model=SomeError)
