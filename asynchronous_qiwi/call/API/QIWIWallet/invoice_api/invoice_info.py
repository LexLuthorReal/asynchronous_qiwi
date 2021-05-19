from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class InvoiceInfoAPI:

    @staticmethod
    async def get_invoice_info(wallet_api_key: str, external_invoice_uid: str) -> dict:
        url = QIWIWalletURLS.Invoice.invoice_statements
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"externalInvoiceId": external_invoice_uid}
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        return response_data
