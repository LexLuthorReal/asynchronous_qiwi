from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class DetectProviderAPI:

    @classmethod
    async def get_provider_phrase(cls, search_phrase: str) -> dict:
        url = QIWIWalletURLS.Payments.detect_phrase.format(search_phrase)
        headers = {"Accept": "application/json",
                   "Cache-Control": "no-cache",
                   "Content-Type": "application/x-www-form-urlencoded"}
        response = await Connector.request(url=url, headers=headers, request_type=POST)
        response_data = await response.json()
        return response_data
