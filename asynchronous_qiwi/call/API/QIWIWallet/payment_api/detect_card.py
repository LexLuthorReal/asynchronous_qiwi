from aiohttp import FormData
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class DetectCardAPI:

    @classmethod
    async def get_card_provider(cls, card_number: str) -> dict:
        url = QIWIWalletURLS.Payments.detect_card
        headers = {"Accept": "application/json",
                   "Cache-Control": "no-cache",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = FormData()
        data.add_field(name="cardNumber", value=card_number)
        response = await Connector.request(url=url, headers=headers, data=data, request_type=POST)
        response_data = await response.json()
        return response_data
