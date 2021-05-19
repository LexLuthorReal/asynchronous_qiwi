from aiohttp import FormData
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class DetectMobileAPI:

    @classmethod
    async def get_mobile_provider(cls, phone_number: str) -> dict:
        url = QIWIWalletURLS.Payments.detect_mobile
        headers = {"Accept": "application/json",
                   "Cache-Control": "no-cache",
                   "Content-Type": "application/x-www-form-urlencoded"}
        data = FormData()
        data.add_field(name="phone", value=phone_number)
        response = await Connector.request(url=url, headers=headers, data=data, request_type=POST)
        response_data = await response.json()
        return response_data
