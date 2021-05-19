import enum


class PayMethodFilter(enum.Enum):

    QIWI = enum.auto()
    LINKED_CARD = enum.auto()
    CARD = enum.auto()
