from typing import Optional
from .....data.URL import QIWIWalletURLS
from .....data_types.QIWIWallet import PaymentTypes
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class TransactionInfoAPI:

    @staticmethod
    async def get_transaction_info(wallet_api_key: str, txn_id: int,
                                   type_operation: Optional[PaymentTypes] = None) -> dict:
        url = QIWIWalletURLS.transaction_info.format(txn_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {}
        if type_operation is not None:
            params["type"] = type_operation.name
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        return response_data
