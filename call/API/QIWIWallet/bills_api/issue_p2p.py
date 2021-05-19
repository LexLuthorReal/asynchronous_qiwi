from typing import Optional
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class IssueP2PTokenAPI:

    @classmethod
    async def issue_p2p_token(cls, wallet_api_key: str, keys_pair_name: str,
                              server_notifications_url: Optional[str] = None) -> dict:
        url = QIWIWalletURLS.Invoice.p2p_issue
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        json = {"keysPairName": keys_pair_name}
        if server_notifications_url is not None:
            json["serverNotificationsUrl"] = server_notifications_url
        response = await Connector.request(url=url, headers=headers, json=json, request_type=POST)
        response_data = await response.json()
        return response_data
