from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class CheckoutInvoiceAPI:

    @staticmethod
    async def checkout_invoice(wallet_api_key: str, invoice_uid: str) -> dict:
        url = QIWIWalletURLS.Invoice.check_invoice_uid.format(invoice_uid)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
