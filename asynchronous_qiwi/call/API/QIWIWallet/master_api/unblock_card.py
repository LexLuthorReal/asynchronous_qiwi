from loguru import logger
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT


class UnblockQVCAPI:

    @classmethod
    async def unblock_qvc(cls, wallet_api_key: str, phone_number: str, card_id: int) -> Union[dict, bool]:
        url = QIWIWalletURLS.QIWIMaster.unblock_card.format(phone_number, card_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        try:
            response = await Connector.request(url=url, headers=headers, request_type=PUT)
            response_data = await response.json()
        except ClientError:
            logger.warning("Some error. Maybe range is big then 90 days or card_id not exist.")
        else:
            return response_data
        return False
