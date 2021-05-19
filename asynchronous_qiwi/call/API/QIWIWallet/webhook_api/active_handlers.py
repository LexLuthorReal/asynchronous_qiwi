from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class ActiveHookHandlersAPI:

    @classmethod
    async def get_active_hook_handlers(cls, wallet_api_key: str) -> dict:
        url = QIWIWalletURLS.WebHooks.active
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET, is_webhook=True)
        response_data = await response.json()
        return response_data
