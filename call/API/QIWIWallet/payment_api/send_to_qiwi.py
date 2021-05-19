from time import time
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST
from .....models.QIWIWallet import Payment, AmountData, AccountField, PaymentMethod


class SendQIWIAPI:

    @classmethod
    async def send_to_qiwi(cls, wallet_api_key: str, target_account: str, comment: str, amount: float,
                           target_currency: int, account_currency: int, method_type: str = "Account") -> dict:
        url = QIWIWalletURLS.Payments.send_to_qiwi
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        payment = Payment(id=str(int(time() * 1000)),
                          sum=AmountData(amount=amount, currency=target_currency),
                          paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                          comment=comment,
                          fields=AccountField(account=target_account))
        response = await Connector.request(url=url, headers=headers, json=payment.dict(by_alias=True),
                                           request_type=POST)
        response_data = await response.json()
        return response_data
