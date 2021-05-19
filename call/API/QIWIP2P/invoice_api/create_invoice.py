import datetime
from .....data.URL import QIWIP2PURLS
from typing import Optional, Dict, Any, List, Set
from .....data_types.QIWIP2P import PaySourcesTypes
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT
from .....utils.tools.datetime_str import DatetimeModule
from .....models.QIWIP2P import CreateInvoice, StandardCustomFields, AmountData, CustomerData


class CreateInvoiceAPI:

    @classmethod
    async def new_invoice(cls, secret_key: str, bill_id: str, amount: float, invoice_currency: str,
                          lifetime: int = 1, comment: Optional[str] = None, phone_customer: Optional[str] = None,
                          email_customer: Optional[str] = None, account_customer: Optional[str] = None,
                          custom_fields: Optional[Dict[str, Any]] = None, theme_code: Optional[str] = None,
                          pay_sources_filter: Optional[List[Set[PaySourcesTypes]]] = None) -> dict:
        url = QIWIP2PURLS.invoice.format(bill_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {secret_key}",
                   "Content-Type": "application/json"}
        if comment is not None:
            if len(comment) > 255:
                raise Exception("Comment length can't be then 255 symbols.")
        if custom_fields is None:
            pay_sources = None
            if pay_sources_filter is not None:
                pay_sources = ""
                for val in pay_sources_filter[0]:
                    pay_sources += val.value + ","
                pay_sources = pay_sources[:-1]
            custom_fields = StandardCustomFields(paySourcesFilter=pay_sources, themeCode=theme_code)
        expiration_date_time = datetime.datetime.now().astimezone() + datetime.timedelta(days=lifetime)
        expiration_date_time = await DatetimeModule.parse_datetime(dt=expiration_date_time)
        invoice = CreateInvoice(amount=AmountData(value=amount, currency=invoice_currency),
                                expirationDateTime=expiration_date_time,
                                customer=CustomerData(phone=phone_customer,
                                                      email=email_customer,
                                                      account=account_customer),
                                comment=comment,
                                customFields=custom_fields)
        response = await Connector.request(url=url, headers=headers,
                                           json=invoice.dict(by_alias=True, exclude_none=True), request_type=PUT)
        response_data = await response.json()
        return response_data
