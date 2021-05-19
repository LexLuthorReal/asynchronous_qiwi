from .....data.URL import QIWIWalletURLS
from typing import Optional, List, Set
from .....data_types.QIWIWallet import LockedFields, AccountTypes


class AutofillFormGenerator:

    @staticmethod
    async def autofill_form(provider_id: int, currency: Optional[int] = None, comment: Optional[str] = None,
                            target_account: Optional[str] = None, amount_integer: Optional[int] = None,
                            amount_fraction: Optional[int] = None, account_type: Optional[AccountTypes] = None,
                            locked_fields: Optional[List[Set[LockedFields]]] = None) -> str:
        url = QIWIWalletURLS.Payments.autofill_form.format(provider_id) + "?"
        if amount_integer is not None or amount_fraction is not None:
            if currency is None:
                raise Exception("The currency parameter cannot be absent for a given amount.")
        if comment is not None:
            if provider_id != 99 and provider_id != 99999:
                raise Exception("comment parameter only for provider ID 99 and 99999.")
        if account_type is not None:
            if provider_id != 99999:
                raise Exception("account_type parameter only for provider ID 99999.")
        blocked = {}
        if locked_fields is not None:
            for i, filed in enumerate(locked_fields[0]):
                blocked[f'blocked[{i}]'] = filed.value
        for k, v in {k: v for k, v in {"amountInteger": amount_integer,
                                       "amountFraction": amount_fraction,
                                       "currency": currency,
                                       "extra['comment']": comment,
                                       "extra['account']": target_account,
                                       **blocked,
                                       "extra['accountType']": account_type.value}.items() if v is not None}.items():
            url += k + "=" + str(v) + "&"
        return url[:-1]
