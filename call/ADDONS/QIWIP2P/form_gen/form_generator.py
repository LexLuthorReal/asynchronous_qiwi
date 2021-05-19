import datetime
from .....data.URL import QIWIP2PURLS
from typing import Optional, Dict, Any, List, Set
from .....data_types.QIWIP2P import PaySourcesTypes
from .....utils.tools.datetime_str import DatetimeModule


class PublicFormGenerator:

    @staticmethod
    async def generate_form(public_key: str, bill_id: Optional[str] = None, amount: Optional[float] = None,
                            phone_customer: Optional[str] = None, email_customer: Optional[str] = None,
                            account_customer: Optional[str] = None, comment: Optional[str] = None,
                            custom_fields: Optional[Dict[str, Any]] = None, theme_code: Optional[str] = None,
                            pay_sources_filter: Optional[List[Set[PaySourcesTypes]]] = None,
                            lifetime: Optional[int] = None, success_url: Optional[str] = None) -> str:
        url = QIWIP2PURLS.generate_form + "?"
        if bill_id is not None:
            if len(bill_id) > 200:
                raise Exception("Length bill_id can't be then 200 symbols.")
        if comment is not None:
            if len(comment) > 255:
                raise Exception("Length comment can't be then 255 symbols.")
        if custom_fields is None:
            pay_sources = None
            if pay_sources_filter is not None:
                pay_sources = ""
                for val in pay_sources_filter[0]:
                    pay_sources += val.value + ","
                pay_sources = pay_sources[:-1]
            custom_fields = {"customFields[paySourcesFilter]": pay_sources,
                             "customFields[themeCode]": theme_code}
        if lifetime is not None:
            lifetime = datetime.datetime.now().astimezone() + datetime.timedelta(days=lifetime)
            lifetime = await DatetimeModule.datetime_str(dt=lifetime, fmt="%Y-%m-%dT%H%M")
        for k, v in {k: v for k, v in {"publicKey": public_key,
                                       "billId": bill_id,
                                       "amount": amount,
                                       "phone": phone_customer,
                                       "email": email_customer,
                                       "account": account_customer,
                                       "comment": comment,
                                       **custom_fields,
                                       "lifetime": lifetime,
                                       "successUrl": success_url}.items() if v is not None}.items():
            url += k + "=" + str(v) + "&"
        return url[:-1]
