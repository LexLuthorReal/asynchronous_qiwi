import enum


class LimitsTypes(enum.Enum):

    """
    REFILL - the maximum allowed account balance
    TURNOVER - monthly turnover
    PAYMENTS_P2P - transfers to other wallets per month
    PAYMENTS_PROVIDER_INTERNATIONALS - payments to foreign companies per month
    PAYMENTS_PROVIDER_PAYOUT - Transfers to bank accounts and cards, wallets of other systems
    WITHDRAW_CASH - cash withdrawals per month. At least one type of operation must be specified.
    ALL_LIMITS - full info about limits - Custom type
    """

    REFILL = enum.auto()
    TURNOVER = enum.auto()
    PAYMENTS_P2P = enum.auto()
    PAYMENTS_PROVIDER_INTERNATIONALS = enum.auto()
    PAYMENTS_PROVIDER_PAYOUT = enum.auto()
    WITHDRAW_CASH = enum.auto()
