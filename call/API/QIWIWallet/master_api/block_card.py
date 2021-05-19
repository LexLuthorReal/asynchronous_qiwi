from loguru import logger
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT


class BlockQVCAPI:

    @classmethod
    async def block_qvc(cls, wallet_api_key: str, phone_number: str, card_id: int) -> bool:
        url = QIWIWalletURLS.QIWIMaster.block_card.format(phone_number, card_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        try:
            await Connector.request(url=url, headers=headers, request_type=PUT)
        except ClientError:
            logger.warning("Some error. Maybe card is blocked or not exist.")
        else:
            return True
        return False
