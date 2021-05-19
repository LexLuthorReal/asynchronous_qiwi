from .....data.URL import QIWIWalletURLS
from .....data_types.connector.request_type import GET
from .....connector.aiohttp_connector import Connector


class CurrencyRatesAPI:

    @classmethod
    async def get_currency_rates(cls, wallet_api_key: str) -> dict:
        url = QIWIWalletURLS.Payments.currency_rates
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
