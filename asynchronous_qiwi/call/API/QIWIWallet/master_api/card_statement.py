from loguru import logger
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....data_types.QIWIWallet import DateRange
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....utils.tools.datetime_str import DatetimeModule


class QVCStatementAPI:

    @classmethod
    async def get_qvc_statement(cls, wallet_api_key: str, phone_number: str, card_id: int,
                                date_range: DateRange) -> Union[bool, bytes]:
        start_date = await DatetimeModule.parse_datetime(dt=date_range.start_date)
        end_date = await DatetimeModule.parse_datetime(dt=date_range.end_date)
        url = QIWIWalletURLS.QIWIMaster.card_statement.format(phone_number, card_id, start_date, end_date)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        try:
            response = await Connector.request(url=url, headers=headers, request_type=GET, is_file=True)
        except ClientError:
            logger.warning(f"Some error. Statement not available, card_id: {card_id}")
        else:
            return response
        return False
