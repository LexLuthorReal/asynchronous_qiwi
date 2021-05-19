import enum


class InvoicesTypes(enum.Enum):

    """
    PAID - paid bills.
    READY_FOR_PAY - created bills.
    EXPIRED - expired bills.
    REJECTED - rejected bills.
    ...
    """

    PAID = enum.auto()
    READY_FOR_PAY = enum.auto()
    EXPIRED = enum.auto()
    REJECTED = enum.auto()
    PAYING = enum.auto()
    ERROR = enum.auto()
    REJECTED_BY_CUSTOMER = enum.auto()
    REJECTED_BY_MERCHANT = enum.auto()
    WAITING = enum.auto()
