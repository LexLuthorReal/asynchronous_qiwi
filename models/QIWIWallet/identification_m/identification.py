from loguru import logger
import datetime
from typing import Optional, Union
from pydantic.fields import ModelField
from pydantic import BaseModel, Field, validator, ValidationError


class Identification(BaseModel):

    """Номер кошелька пользователя"""
    id: Optional[int] = Field(None, alias="id")

    """Имя пользователя"""
    first_name: Optional[str] = Field(..., alias="firstName")

    """Отчество пользователя"""
    middle_name: Optional[str] = Field(..., alias="middleName")

    """Фамилия пользователя"""
    last_name: Optional[str] = Field(..., alias="lastName")

    """Дата рождения пользователя (в формате "ГГГГ-ММ-ДД") - 0000-00-00"""
    birth_date: Optional[Union[str, datetime.date]] = Field(..., alias="birthDate")

    """Серия и номер паспорта пользователя (только цифры) - 1111111111"""
    passport: Optional[str] = Field(..., alias="passport")

    """ИНН пользователя"""
    inn: Optional[str] = Field(..., alias="inn")

    """Номер СНИЛС пользователя"""
    snils: Optional[str] = Field(..., alias="snils")

    """Номер полиса ОМС пользователя"""
    oms: Optional[str] = Field(..., alias="oms")

    """
    Текущий уровень идентификации кошелька:
    SIMPLE - без идентификации.
    VERIFIED - упрощенная идентификация (данные для идентификации успешно прошли проверку).
    FULL – если кошелек уже ранее получал полную идентификацию по данным ФИО, номеру паспорта и дате рождения.
    """
    type: Optional[str] = Field(..., alias="type")

    @validator('birth_date')
    def birth_date_datetime(cls, birth_date: Optional[Union[str, datetime.date]],
                            field: ModelField) -> Optional[datetime.date]:
        if isinstance(birth_date, str):
            try:
                birth_date = datetime.datetime.date(datetime.datetime.strptime(birth_date, "%Y-%m-%d"))
            except ValueError as e:
                logger.warning(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return birth_date
        elif isinstance(birth_date, datetime.date):
            return birth_date
        elif birth_date is None:
            return birth_date
        raise ValidationError(model=Identification)


class SendIdentification(BaseModel):

    """Имя пользователя"""
    first_name: str = Field(..., alias="firstName")

    """Отчество пользователя"""
    middle_name: str = Field(..., alias="middleName")

    """Фамилия пользователя"""
    last_name: str = Field(..., alias="lastName")

    """Дата рождения пользователя (в формате "ГГГГ-ММ-ДД") - 0000-00-00"""
    birth_date: Union[datetime.date, str] = Field(..., alias="birthDate")

    """Серия и номер паспорта пользователя (только цифры) - 1111111111"""
    passport: str = Field(..., alias="passport")

    # ЭТИ ПАРАМЕТРЫ НЕ ОБЯЗАТЕЛЬНЫ К ИСПОЛЬЗОВАНИЮ, ИНАЧЕ УКАЗЫВАТЬ ПОЛНОСТЬЮ

    """ИНН пользователя"""
    inn: Optional[str] = Field(None, alias="inn")

    """Номер СНИЛС пользователя"""
    snils: Optional[str] = Field(None, alias="snils")

    """Номер полиса ОМС пользователя"""
    oms: Optional[str] = Field(None, alias="oms")

    @validator('birth_date')
    def birth_date_datetime(cls, birth_date: Union[str, datetime.date], field: ModelField) -> str:
        if isinstance(birth_date, str):
            try:
                datetime.datetime.date(datetime.datetime.strptime(birth_date, "%Y-%m-%d"))
            except ValueError as e:
                logger.exception(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return birth_date
        elif isinstance(birth_date, datetime.date):
            try:
                birth_date = birth_date.strftime("%Y-%m-%d")
            except ValueError as e:
                logger.exception(f"[VALIDATION CONVERT] {field.name.upper()}: " + str(e))
            else:
                return birth_date
        raise ValidationError(model=SendIdentification)
