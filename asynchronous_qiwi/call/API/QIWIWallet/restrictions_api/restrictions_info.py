from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class UserRestrictionsAPI:

    @staticmethod
    async def get_restrictions(wallet_api_key: str, phone_number: str) -> dict:
        url = QIWIWalletURLS.restrictions.format(phone_number)
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
