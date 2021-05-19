import enum


class HookType(enum.Enum):

    """
    WEB - WEBHOOK type.
    """

    WEB = 1


class NotifyType(enum.Enum):

    """
    0 - only incoming transactions (replenishment).
    1 - only outgoing transactions (payments).
    2 - all transactions.
    """

    IN = 0
    OUT = 1
    BOTH = 2
