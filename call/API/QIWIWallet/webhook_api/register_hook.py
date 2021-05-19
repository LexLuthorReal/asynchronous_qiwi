from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT
from .....data_types.QIWIWallet import HookType, NotifyType


class RegistrationHookAPI:

    @classmethod
    async def register_hook(cls, wallet_api_key: str, hook_type: HookType, url_hook: str,
                            notify_type: NotifyType) -> dict:
        if len(url_hook) <= 100:
            url = QIWIWalletURLS.WebHooks.register
            headers = {"Accept": "application/json",
                       "Authorization": f"Bearer {wallet_api_key}"}
            params = {"hookType": hook_type.value,
                      "param": url_hook,
                      "txnType": notify_type.value}
        else:
            raise Exception("The length must not exceed 100 characters.")
        response = await Connector.request(url=url, headers=headers, params=params, request_type=PUT, is_webhook=True)
        response_data = await response.json()
        return response_data
