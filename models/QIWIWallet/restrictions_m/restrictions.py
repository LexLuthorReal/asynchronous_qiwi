from typing import Optional, List, Union

from pydantic import BaseModel, Field


class RestrictionType(BaseModel):

    restriction_code: str = Field(..., alias="restrictionCode")
    restriction_description: str = Field(..., alias="restrictionDescription")


class Restrictions(BaseModel):
    restrictions: Optional[List[Union[RestrictionType]]] = Field(...)
