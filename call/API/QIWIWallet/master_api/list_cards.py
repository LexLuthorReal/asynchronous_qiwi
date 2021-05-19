from .....data.URL import QIWIWalletURLS
from .....data_types.QIWIWallet import CardAlias
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class ListQVCAPI:

    @staticmethod
    async def get_list_qvc_master(wallet_api_key: str) -> dict:
        url = QIWIWalletURLS.QIWIMaster.list_card.format(CardAlias.QVC_MASTER.value)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=POST)
        response_data = await response.json()
        return response_data
