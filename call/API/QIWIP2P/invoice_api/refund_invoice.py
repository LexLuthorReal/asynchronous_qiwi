from .....data.URL import QIWIP2PURLS
from .....models.QIWIP2P import AmountData
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT


class RefundInvoiceAPI:

    @classmethod
    async def refund_invoice(cls, secret_key: str, bill_id: str, refund_id: str, amount: float,
                             return_currency: str) -> dict:
        url = QIWIP2PURLS.refund.format(bill_id, refund_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {secret_key}",
                   "Content-Type": "application/json"}
        json = AmountData(currency=return_currency,
                          value=amount)
        response = await Connector.request(url=url, headers=headers, json=json, request_type=PUT)
        response_data = await response.json()
        return response_data
