from loguru import logger
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import PATCH


class DefaultBalanceAPI:

    @staticmethod
    async def set_default_balance(wallet_api_key: str, phone_number: str, balance_alias: str) -> bool:
        url = QIWIWalletURLS.Balance.set_new_balance.format(phone_number, balance_alias)
        headers = {"Accept": "application/json",
                   "Content-type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        json = {"defaultAccount": True}
        try:
            await Connector.request(url=url, headers=headers, json=json, request_type=PATCH)
        except ClientError:
            logger.warning(f"This balance is default now or some another error: {balance_alias}")
        else:
            return True
        return False
