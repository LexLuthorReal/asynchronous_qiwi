import enum


class PaySourcesTypes(enum.Enum):

    """
    QW - QIWI Wallet.
    CARD - bank card.
    ...
    """

    QW = "qw"
    CARD = "card"
    MOBILE = "mobile"
