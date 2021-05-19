from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class UserInfoAPI:

    @staticmethod
    async def get_me(wallet_api_key: str, auth_info_enabled: bool = True,
                     contract_info_enabled: bool = True, user_info_enabled: bool = True) -> dict:
        url = QIWIWalletURLS.me
        headers = {"Accept": "application/json",
                   "Content-Type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"authInfoEnabled": f"{auth_info_enabled}",
                  "contractInfoEnabled": f"{contract_info_enabled}",
                  "userInfoEnabled": f"{user_info_enabled}"}
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        return response_data
