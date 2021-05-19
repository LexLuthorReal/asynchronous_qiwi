from time import time
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import POST
from .....models.QIWIWallet import Payment, AmountData, PaymentMethod, FreeDetails


class FreePaymentsAPI:

    @classmethod
    async def payment_free_details(cls, wallet_api_key: str, target_account: str, amount: float,
                                   target_currency: int, account_currency: int, name_bank: str, bik_recipient: int,
                                   city_recipient: str, name_organization: str, inn_organization: int,
                                   kpp_organization: int, nds: str, goal_payment: str, payer_name: str,
                                   payer_surname: str, payer_patronymic: str, request_protocol: str = "qw1",
                                   service_id: int = 1717, urgent_payment: int = 0, is_commercial: int = 1,
                                   info: str = "Коммерческие организации", method_type: str = "Account") -> dict:
        url = QIWIWalletURLS.Payments.payments.format(1717)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}",
                   "Content-Type": "application/json"}
        payment = Payment(id=str(int(time() * 1000)),
                          sum=AmountData(amount=amount, currency=target_currency),
                          paymentMethod=PaymentMethod(type=method_type, accountId=account_currency),
                          comment=None,
                          fields=FreeDetails(extra_to_bik=bik_recipient,
                                             request_protocol=request_protocol,
                                             city=city_recipient,
                                             name=name_bank,
                                             to_bik=bik_recipient,
                                             urgent=urgent_payment,
                                             to_kpp=kpp_organization,
                                             is_commercial=is_commercial,
                                             nds=nds,
                                             goal=goal_payment,
                                             from_name_p=payer_patronymic,
                                             from_name=payer_name,
                                             from_name_f=payer_surname,
                                             info=info,
                                             to_name=name_organization,
                                             to_inn=inn_organization,
                                             account=target_account,
                                             to_service_id=service_id))
        response = await Connector.request(url=url,
                                           headers=headers,
                                           json=payment.dict(by_alias=True, exclude_none=True),
                                           request_type=POST)
        response_data = await response.json()
        return response_data
