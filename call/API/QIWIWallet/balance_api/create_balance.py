from loguru import logger
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class CreateBalanceAPI:

    @staticmethod
    async def create_balance(wallet_api_key: str, phone_number: str, alias: str) -> bool:
        url = QIWIWalletURLS.Balance.balance.format(phone_number)
        headers = {"Accept": "application/json",
                   "Content-type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        json = {"alias": alias}
        try:
            await Connector.request(url=url, headers=headers, json=json, request_type=POST)
        except ClientError:
            logger.warning(f"You can't create balance with this alias or this alias is created: {alias}")
        else:
            return True
        return False
