from loguru import logger
from uuid import UUID
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT


class QVCDetailsAPI:

    @classmethod
    async def get_qvc_details(cls, wallet_api_key: str, card_id: int, operation_id: UUID) -> Union[dict, bool]:
        url = QIWIWalletURLS.QIWIMaster.card_details.format(card_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        json = {"operationId": operation_id.__str__()}
        try:
            response = await Connector.request(url=url, headers=headers, json=json, request_type=PUT)
            response_data = await response.json()
        except ClientError:
            logger.warning("Some error. Maybe card_id does not exist.")
        else:
            return response_data
        return False
