import enum


class LockedFields(enum.Enum):

    """
    SUM - field "payment amount".
    ACCOUNT - field "account/phone/card number"
    COMMENT - the "comment" field.
    """

    SUM = "sum"
    ACCOUNT = "account"
    COMMENT = "comment"


class AccountTypes(enum.Enum):

    """
    PHONE - for transfer by number.
    NICKNAME - to translate by nickname.
    """

    PHONE = "phone"
    NICKNAME = "nickname"
