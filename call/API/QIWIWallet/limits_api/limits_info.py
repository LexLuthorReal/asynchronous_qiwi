from typing import List, Set, Optional
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....data_types.QIWIWallet.limits import LimitsTypes


class LimitsInfoAPI:

    @staticmethod
    async def get_limits(wallet_api_key: str, phone_number: str,
                         type_limits: Optional[List[Set[LimitsTypes]]] = None) -> dict:
        url = QIWIWalletURLS.limits.format(phone_number)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {}
        if type_limits is None:
            for i, operation in enumerate(LimitsTypes):
                params[f'types[{i}]'] = operation.name
            response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
            response_data = await response.json()
            return response_data
        else:
            for i, operation in enumerate(type_limits[0]):
                params[f'types[{i}]'] = operation.name
            response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
            response_data = await response.json()
            return response_data
