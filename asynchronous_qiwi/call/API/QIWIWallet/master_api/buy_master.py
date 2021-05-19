from loguru import logger
from time import time
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....data_types.QIWIWallet import CardAlias
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST
from .....models.QIWIWallet import (
    Payment, AmountData, PaymentMethod, QIWIMasterFields
)


class BuyQIWIMasterAPI:

    @staticmethod
    async def buy_qiwi_master(wallet_api_key: str, phone_number: str, comment: str,
                              master_price: int = 2999, payment_currency: int = 643,
                              method_type: str = "Account", account_currency: int = 643) -> Union[dict, bool]:
        url = QIWIWalletURLS.QIWIMaster.QIWI_Master_package
        headers = {"Accept": "application/json",
                   "Content-type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        payment = Payment(id=str(int(time() * 1000)),
                          sum=AmountData(amount=master_price, currency=payment_currency),
                          paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                          comment=comment,
                          fields=QIWIMasterFields(account=phone_number, vas_alias=CardAlias.QVC_MASTER.value))
        try:
            response = await Connector.request(url=url, headers=headers, json=payment.dict(by_alias=True),
                                               request_type=POST)
            response_data = await response.json()
        except ClientError:
            logger.warning("Not enough balance.")
        else:
            return response_data
        return False
