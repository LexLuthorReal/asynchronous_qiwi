import enum


class PaymentTypes(enum.Enum):

    IN = enum.auto()
    OUT = enum.auto()
    QIWI_CARD = enum.auto()


class PaymentSources(enum.Enum):

    QW_RUB = enum.auto()
    QW_USD = enum.auto()
    QW_EUR = enum.auto()
    CARD = enum.auto()
    MK = enum.auto()


class PaymentStatuses(enum.Enum):

    WAITING = enum.auto()
    SUCCESS = enum.auto()
    ERROR = enum.auto()
