from .....data.URL import QIWIP2PURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class RefundStatusAPI:

    @classmethod
    async def refund_status(cls, secret_key: str, bill_id: str, refund_id: str) -> dict:
        url = QIWIP2PURLS.refund.format(bill_id, refund_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {secret_key}"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
