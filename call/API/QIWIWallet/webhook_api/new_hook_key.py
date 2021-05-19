from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class NewHookSignKeyAPI:

    @classmethod
    async def new_hook_sign_key(cls, wallet_api_key: str, hook_id: str) -> dict:
        url = QIWIWalletURLS.WebHooks.new_sign_key.format(hook_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=POST, is_webhook=True)
        response_data = await response.json()
        return response_data
