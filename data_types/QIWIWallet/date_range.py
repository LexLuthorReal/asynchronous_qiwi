import datetime
from typing import Union
from pydantic import BaseModel, Field, root_validator


class DateRange(BaseModel):
    """
    Object: dateRange for get payments of this range
    You can set startDate & endDate with parse any object with this alias
    Or set using this Instance with alias arguments
    """

    start_date: Union[datetime.datetime] = Field(..., alias="startDate")
    end_date: Union[datetime.datetime] = Field(..., alias="endDate")

    @root_validator(pre=True)
    def data_range_validator(cls, values: dict):
        start_date, end_date = values.get("startDate"), values.get("endDate")
        date_range = end_date - start_date
        if date_range.days > 90:
            raise Exception("Max date range is 90 days.")
        elif date_range.days < 0:
            raise Exception("Date range can't be small then 0 days.")
        values["startDate"] = start_date
        values["endDate"] = end_date
        return values
