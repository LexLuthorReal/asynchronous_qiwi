from .....data.URL import QIWIP2PURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class RejectInvoiceAPI:

    @classmethod
    async def reject_invoice(cls, secret_key: str, bill_id: str) -> dict:
        url = QIWIP2PURLS.invoice.format(bill_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {secret_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
