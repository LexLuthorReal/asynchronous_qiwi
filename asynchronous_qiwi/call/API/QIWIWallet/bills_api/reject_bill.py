from loguru import logger
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST


class BillRejectAPI:

    @classmethod
    async def reject_unpaid_bill(cls, wallet_api_key: str, bill_id: int) -> bool:
        url = QIWIWalletURLS.Bills.pay_bill
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        json = {"id": bill_id}
        try:
            await Connector.request(url=url, headers=headers, json=json, request_type=POST)
        except ClientError:
            logger.warning(f"Some problem, maybe bill is paid.")
        else:
            return True
        return False
