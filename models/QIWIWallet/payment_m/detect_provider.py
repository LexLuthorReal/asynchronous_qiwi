from loguru import logger
from pydantic.fields import ModelField
from typing import Optional, Union, List
from pydantic import BaseModel, Field, validator, ValidationError


class CodeData(BaseModel):

    value: Union[str, int] = Field(..., alias="value")
    name: str = Field(..., alias="_name")

    @validator('value')
    def value_int(cls, value: Union[str, int], field: ModelField) -> Union[int, str]:
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
                return value
            finally:
                return value
        elif isinstance(value, int):
            return value
        raise ValidationError(model=CodeData)


class ProviderType(BaseModel):

    id: str = Field(..., alias="id")
    new: bool = Field(..., alias="new")
    name: str = Field(..., alias="_name")


class ProviderID(BaseModel):

    id: Union[str, int] = Field(..., alias="id")
    type: ProviderType = Field(..., alias="type")

    @validator('id')
    def id_int(cls, str_id: Union[str, int], field: ModelField) -> Union[str, int]:
        if isinstance(str_id, str):
            try:
                str_id = int(str_id)
            except ValueError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
                return str_id
            finally:
                return str_id
        elif isinstance(str_id, int):
            return str_id
        raise ValidationError(model=ProviderID)


class ProviderItem(BaseModel):

    id: ProviderID = Field(..., alias="id")
    image: Optional[str] = Field(..., alias="image")
    key: ProviderID = Field(..., alias="key")
    new: bool = Field(..., alias="new")
    text: str = Field(..., alias="text")
    type: ProviderType = Field(..., alias="type")
    url: Optional[str] = Field(..., alias="url")


class ProviderItems(BaseModel):

    item: ProviderItem = Field(..., alias="item")
    logo: str = Field(..., alias="logo")


class PagingSizes(BaseModel):

    id: Union[str, int] = Field(..., alias="id")
    label: Union[str, int] = Field(..., alias="label")
    value: Union[str, int] = Field(..., alias="value")

    @validator('id')
    def id_int(cls, str_id: Union[str, int]) -> Union[str, int]:
        if isinstance(str_id, str):
            try:
                str_id = int(str_id)
            except ValueError:
                return str_id
            finally:
                return str_id
        elif isinstance(str_id, int):
            return str_id
        raise ValidationError(model=PagingSizes)

    @validator('label')
    def label_int(cls, str_label: Union[str, int]) -> Union[str, int]:
        if isinstance(str_label, str):
            try:
                str_label = int(str_label)
            except ValueError:
                return str_label
            finally:
                return str_label
        elif isinstance(str_label, int):
            return str_label
        raise ValidationError(model=PagingSizes)

    @validator('value')
    def value_int(cls, str_value: Union[str, int]) -> Union[str, int]:
        if isinstance(str_value, str):
            try:
                str_value = int(str_value)
            except ValueError:
                return str_value
            finally:
                return str_value
        elif isinstance(str_value, int):
            return str_value
        raise ValidationError(model=PagingSizes)


class Paging(BaseModel):

    current_number: int = Field(..., alias="currentNumber")
    page_count: int = Field(..., alias="pageCount")
    pages: List[Union[int]] = Field(..., alias="pages")
    size: int = Field(..., alias="size")
    size_element_id: Union[str, int] = Field(..., alias="sizeElementId")
    sizes: List[Union[PagingSizes]] = Field(..., alias="sizes")

    @validator('size_element_id')
    def size_element_id_int(cls, size_element_id: Union[str, int], field: ModelField) -> Union[int, str]:
        if isinstance(size_element_id, str):
            try:
                size_element_id = int(size_element_id)
            except ValueError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
                return size_element_id
            finally:
                return size_element_id
        elif isinstance(size_element_id, int):
            return size_element_id
        raise ValidationError(model=Paging)


class ProvidersInfo(BaseModel):

    additional_data: Optional[str] = Field(..., alias="additionalData")
    application_context: Optional[str] = Field(..., alias="applicationContext")
    component: Optional[str] = Field(..., alias="component")
    empty_message: Optional[str] = Field(..., alias="emptyMessage")
    extra_data: Optional[str] = Field(..., alias="extraData")
    items: Optional[List[Union[ProviderItems]]] = Field(..., alias="items")
    paging: Optional[Paging] = Field(..., alias="paging")
    use_suggestion: bool = Field(..., alias="useSuggestion")


class ProviderData(BaseModel):

    code: CodeData = Field(..., alias="code")
    data: Optional[ProvidersInfo] = Field(..., alias="data")
    message: Optional[Union[str, int]] = Field(..., alias="message")
    messages: Optional[Union[dict, str]] = Field(..., alias="messages")

    @validator('message')
    def message_int(cls, message: Optional[Union[str, int]]) -> Optional[Union[str, int]]:
        if isinstance(message, str):
            try:
                message = int(message)
            except ValueError:
                return message
            finally:
                return message
        elif isinstance(message, int):
            return message
        elif message is None:
            return message
        raise ValidationError(model=ProviderData)
