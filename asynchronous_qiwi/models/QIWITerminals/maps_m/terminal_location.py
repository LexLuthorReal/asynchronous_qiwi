import datetime
from loguru import logger
from pydantic.fields import ModelField
from typing import List, Union, Optional
from ....utils.tools.str_datetime import convert
from ....data_types.QIWITerminals import IdentificationMethods
from pydantic import BaseModel, Field, validator, ValidationError


class Coordinate(BaseModel):
    latitude: float = Field(..., alias="latitude")
    longitude: float = Field(..., alias="longitude")
    precision: int = Field(..., alias="precision")


class TerminalLocation(BaseModel):
    terminal_id: int = Field(..., alias="terminalId")
    ttp_id: int = Field(..., alias="ttpId")
    last_active: Optional[Union[str, datetime.datetime]] = Field(..., alias="lastActive")
    count: int = Field(..., alias="count")
    coordinate: Coordinate = Field(..., alias="coordinate")
    address: str = Field(..., alias="address")
    verified: bool = Field(..., alias="verified")
    label: str = Field(..., alias="label")
    description: Optional[str] = Field(..., alias="description")
    cash_allowed: bool = Field(..., alias="cashAllowed")
    card_allowed: bool = Field(..., alias="cardAllowed")
    identification_type: Union[int, IdentificationMethods] = Field(..., alias="identificationType")

    @validator('last_active')
    def last_active_datetime(cls, last_active: Optional[Union[str, datetime.datetime]],
                             field: ModelField) -> Optional[datetime.datetime]:
        if isinstance(last_active, str):
            if "." in last_active:
                last_active = convert(value=last_active, validator_name=field.name.upper(),
                                      format_str="%Y-%m-%dT%H:%M:%S.%f")
            else:
                last_active = convert(value=last_active, validator_name=field.name.upper(),
                                      format_str="%Y-%m-%dT%H:%M:%S")
            return last_active
        elif isinstance(last_active, datetime.datetime):
            return last_active
        elif last_active is None:
            return last_active
        raise ValidationError(model=TerminalLocation)

    @validator('identification_type')
    def identification_type_types(cls, identification_type: Union[int, IdentificationMethods],
                                  field: ModelField) -> IdentificationMethods:
        if isinstance(identification_type, int):
            try:
                identification_type = IdentificationMethods(identification_type)
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return identification_type
        elif isinstance(identification_type, IdentificationMethods):
            return identification_type
        raise ValidationError(model=TerminalLocation)


class TerminalResult(BaseModel):
    result: List[Union[TerminalLocation]] = Field(...)


class SearchTerminal(BaseModel):
    latitude_nw: float = Field(..., alias="latNW")
    longitude_nw: float = Field(..., alias="lngNW")
    latitude_se: float = Field(..., alias="latSE")
    longitude_se: float = Field(..., alias="lngSE")
    zoom: Optional[int] = Field(..., alias="zoom")
    active_within_minutes: Optional[float] = Field(..., alias="activeWithinMinutes")
    with_refill_wallet: Optional[bool] = Field(..., alias="withRefillWallet")
    ttp_ids: Optional[List[int]] = Field(..., alias="ttpIds")
    cash_allowed: Optional[bool] = Field(..., alias="cacheAllowed")
    card_allowed: Optional[bool] = Field(..., alias="cardAllowed")
    identification_types: Optional[List[Union[IdentificationMethods, int]]] = Field(..., alias="identificationTypes")
    ttp_groups: Optional[List[int]] = Field(..., alias="ttpGroups")

    @validator("zoom")
    def zoom_range(cls, zoom: Optional[int]) -> Optional[int]:
        if zoom is None:
            return zoom
        elif zoom in range(18):
            return zoom
        raise ValidationError(model=SearchTerminal)

    @validator('identification_types')
    def identification_types_types(cls, identification_types: Optional[List[IdentificationMethods]],
                                   field: ModelField) -> Optional[List[int]]:
        if isinstance(identification_types, List):
            try:
                identification_types = [v.value for v in identification_types]
            except KeyError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return identification_types
        elif identification_types is None:
            return identification_types
        raise ValidationError(model=SearchTerminal)
