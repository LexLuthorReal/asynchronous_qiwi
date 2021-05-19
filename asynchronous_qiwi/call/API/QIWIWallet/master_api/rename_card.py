from loguru import logger
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PUT


class RenameQVCAPI:

    @classmethod
    async def rename_qvc(cls, wallet_api_key: str, card_id: int, alias: str) -> Union[dict, bool]:
        url = QIWIWalletURLS.QIWIMaster.rename_card.format(card_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        json = {"alias": alias}
        try:
            response = await Connector.request(url=url, headers=headers, json=json, request_type=PUT)
            response_data = await response.json()
        except ClientError:
            logger.warning("Some error. Wrong card_id or alias not permitted.")
        else:
            return response_data
        return False
