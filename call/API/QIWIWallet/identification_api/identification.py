from loguru import logger
from aiohttp import ClientError
from typing import Optional, Union
from .....data.URL import QIWIWalletURLS
from .....models.QIWIWallet import SendIdentification
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET, POST


class IdentificationAPI:

    @staticmethod
    async def identification(wallet_api_key: str, phone_number: str,
                             identification_class: Optional[SendIdentification] = None) -> Union[dict, bool]:
        url = QIWIWalletURLS.identification.format(phone_number)

        if identification_class is None:
            headers = {"Accept": "application/json",
                       "Authorization": f"Bearer {wallet_api_key}"}
            response = await Connector.request(url=url, headers=headers, request_type=GET)
            response_data = await response.json()
            return response_data
        else:
            headers = {"Accept": "application/json",
                       "Content-Type": "application/json",
                       "Authorization": f"Bearer {wallet_api_key}"}
            try:
                response = await Connector.request(url=url, headers=headers,
                                                   json=identification_class.dict(by_alias=True), request_type=POST)
                response_data = await response.json()
            except ClientError:
                logger.warning("You entered wrong data.")
            else:
                return response_data
            return False
