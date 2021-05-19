from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import DELETE


class RemoveHookAPI:

    @classmethod
    async def remove_hook(cls, wallet_api_key: str, hook_id: str) -> dict:
        url = QIWIWalletURLS.WebHooks.remove.format(hook_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=DELETE, is_webhook=True)
        response_data = await response.json()
        return response_data
