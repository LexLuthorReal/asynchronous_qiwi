import enum


class StatusesQVC(enum.Enum):

    OK = enum.auto()
    FAIL = enum.auto()
    CONFIRMATION_REQUIRED = enum.auto()
    CONFIRMATION_LIMIT_EXCEED = enum.auto()
