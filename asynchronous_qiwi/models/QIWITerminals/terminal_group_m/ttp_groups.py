from loguru import logger
from typing import List, Union
from pydantic.fields import ModelField
from ....data_types.QIWITerminals import GroupPartner
from pydantic import BaseModel, Field, validator, ValidationError


class Partner(BaseModel):

    title: str = Field(..., alias="title")
    id: int = Field(..., alias="id")
    maps: List[str] = Field(..., alias="maps")

    @validator('maps')
    def maps_types(cls, maps: Union[List[str], List[GroupPartner]], field: ModelField) -> List[GroupPartner]:
        if isinstance(maps, List):
            try:
                maps = [GroupPartner[v] for v in maps]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return maps
        elif isinstance(maps[0], GroupPartner):
            return maps
        raise ValidationError(model=Partner)


class PartnerResult(BaseModel):
    result: List[Union[Partner]] = Field(...)
