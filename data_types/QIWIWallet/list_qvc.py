import enum


class CardAlias(enum.Enum):

    QVC_CPA = "qvc-cpa"
    QVC_MASTER = "qvc-master"
    QVC_CPA_DEBIT = "qvc-cpa-debit"


class CardStatus(enum.Enum):

    DRAFT = enum.auto()
    COMPLETED = enum.auto()
    PAYMENT_REQUIRED = enum.auto()


class ReleasedCardStatus(enum.Enum):

    ACTIVE = enum.auto()
    SENDED_TO_BANK = enum.auto()
    SENDED_TO_USER = enum.auto()
    BLOCKED = enum.auto()
    UNKNOWN = enum.auto()


class CardType(enum.Enum):

    VIRTUAL = enum.auto()
