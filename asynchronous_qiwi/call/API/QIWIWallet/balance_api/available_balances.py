from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class AvailableBalancesAPI:

    @staticmethod
    async def get_available_balances(wallet_api_key: str, phone_number: str) -> dict:
        url = QIWIWalletURLS.Balance.available_aliases.format(phone_number)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
