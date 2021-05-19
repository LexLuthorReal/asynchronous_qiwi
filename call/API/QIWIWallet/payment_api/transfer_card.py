from loguru import logger
from time import time
from typing import Optional
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST
from .....models.QIWIWallet import Payment, CardFields, AmountData, AccountField, PaymentMethod

ru_banks = [1963, 21013, 31652, 22351]
foreign_banks = [1960, 21012]

"""
1963: "Transfer to a Visa card (Russian bank cards).",
21013: "Transfer to MasterCard (Russian bank cards).",
31652: "Transfer to the card of the national payment system MIR.",
22351: "Transfer to the QVC.",
1960: "Transfer to a Visa card (international transfer)",
21012: "Transfer to MasterCard (international transfer)"
"""


class TransferCardAPI:

    @classmethod
    async def transfer_to_card(cls, wallet_api_key: str, provider_id: int, target_card: str, amount: float,
                               target_currency: int, account_currency: int, method_type: str = "Account",
                               sender_address: Optional[str] = None, sender_city: Optional[str] = None,
                               sender_country: Optional[str] = None, receiver_name: Optional[str] = None,
                               receiver_surname: Optional[str] = None, sender_name: Optional[str] = None,
                               sender_surname: Optional[str] = None) -> dict:
        url = QIWIWalletURLS.Payments.payments.format(provider_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        if provider_id in sorted(ru_banks + foreign_banks):
            payment = Payment(id=str(int(time() * 1000)),
                              sum=AmountData(amount=amount, currency=target_currency),
                              paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                              comment=None,
                              fields=AccountField(account=target_card))
            if provider_id in foreign_banks:
                payment.fields = CardFields(account=target_card,
                                            rec_address=sender_address,
                                            rec_city=sender_city,
                                            rec_country=sender_country,
                                            reg_name=receiver_name,
                                            reg_name_f=receiver_surname,
                                            rem_name=sender_name,
                                            rem_name_f=sender_surname)
            response = await Connector.request(url=url,
                                               headers=headers,
                                               json=payment.dict(by_alias=True, exclude_none=True),
                                               request_type=POST)
            response_data = await response.json()
            return response_data
        else:
            logger.warning("Transfer to the card of this bank is not possible.")
