from loguru import logger
from time import time
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....models.QIWIWallet import VirtualCard
from .....connector.aiohttp_connector import Connector
from .....data_types.QIWIWallet import CardAlias, CardStatus
from .....data_types.connector.request_type import POST, PUT
from .....models.QIWIWallet import (
    Payment, PaymentMethod, AmountData, BuyVirtualCardFields
)


class IssueQVC:

    @staticmethod
    async def issue_qvc(wallet_api_key: str, phone_number: str, card_alias: CardAlias,
                        method_type: str = "Account", account_currency: int = 643) -> Union[VirtualCard, dict, bool]:
        url = QIWIWalletURLS.QIWIMaster.create_virtual_card_order.format(phone_number)
        headers = {"Accept": "application/json",
                   "Content-type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        json = {"cardAlias": card_alias.value}
        # Step 1. Create an order
        try:
            response = await Connector.request(url=url, headers=headers, json=json, request_type=POST)
            response_data = await response.json()
            response_data = VirtualCard(**response_data)
        except ClientError:
            logger.warning(f"Some problem with creation order: {card_alias.value}")
        else:
            # Step 2. Order confirmation
            url = QIWIWalletURLS.QIWIMaster.confirmation_order.format(phone_number, response_data.id)
            try:
                response = await Connector.request(url=url, headers=headers, request_type=PUT)
                response_data = await response.json()
                response_data = VirtualCard(**response_data)
            except ClientError:
                logger.warning(f"Some problem with order confirmation: {card_alias.value}")
            else:
                if response_data.status.value is CardStatus.COMPLETED.value:
                    # Return response (if card is free)
                    return response_data
                elif response_data.status.value is CardStatus.PAYMENT_REQUIRED.value:
                    # Step 3. Buying a card
                    url = QIWIWalletURLS.QIWIMaster.buy_virtual_card
                    payment = \
                        Payment(id=str(int(time() * 1000)),
                                sum=AmountData(amount=response_data.price.amount,
                                               currency=response_data.price.currency),
                                paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                                comment=None,
                                fields=BuyVirtualCardFields(account=phone_number, order_id=response_data.id))
                    try:
                        response = await Connector.request(url=url, headers=headers,
                                                           json=payment.dict(by_alias=True, exclude_none=True),
                                                           request_type=POST)
                        response_data = await response.json()
                    except ClientError:
                        logger.warning("Some error with buy maybe insufficient funds.")
                    else:
                        return response_data
        return False
