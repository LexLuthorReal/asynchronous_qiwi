from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class BillPayAPI:

    @classmethod
    async def pay_bill(cls, wallet_api_key: str, bill_id: int, account_currency: int) -> dict:
        url = QIWIWalletURLS.Bills.pay_bill
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        json = {"invoice_uid": f"{bill_id}",
                "currency": f"{account_currency}"}
        response = await Connector.request(url=url, headers=headers, json=json, request_type=POST)
        response_data = await response.json()
        return response_data
