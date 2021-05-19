from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST
from .....models.QIWIWallet import (
    Commission, PaymentMethod, PurchaseTotals, AmountData
)


class CommissionAPI:

    @classmethod
    async def get_commission(cls, wallet_api_key: str, provider_id: int, target_account: str, amount: float,
                             target_currency: int, account_currency: int, method_type: str = "Account") -> dict:
        url = QIWIWalletURLS.Payments.commission.format(provider_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        commission = Commission(account=target_account,
                                paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                                purchaseTotals=PurchaseTotals(
                                    total=AmountData(amount=amount, currency=target_currency)
                                ))
        response = await Connector.request(url=url,
                                           headers=headers,
                                           json=commission.dict(by_alias=True),
                                           request_type=POST)
        response_data = await response.json()
        return response_data
