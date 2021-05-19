import re
from loguru import logger
from typing import Union
from aiohttp import ClientError
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET, POST
from .....data_types.QIWIWallet import PaymentTypes, ReceiptFormat


class ReceiptAPI:

    @staticmethod
    async def get_payment_receipt_file(wallet_api_key: str, txn_id: int, type_operation: PaymentTypes,
                                       file_format: ReceiptFormat) -> Union[bool, bytes]:
        url = QIWIWalletURLS.receipt_file.format(txn_id)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"type": type_operation.name,
                  "format": file_format.name}
        try:
            response = await Connector.request(url=url, headers=headers, params=params, request_type=GET, is_file=True)
        except ClientError:
            logger.warning(f"Cheque is not available (txnId: {txn_id}, type: {type_operation.name})")
        else:
            return response
        return False

    @staticmethod
    async def send_payment_receipt_email(wallet_api_key: str, txn_id: int,
                                         type_operation: PaymentTypes, email: str) -> bool:
        regex = re.compile(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:"
                           r"[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")"
                           r"@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|"
                           r"\[(?:(\?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])"
                           r"|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:"
                           r"[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\\])")
        if not re.search(regex, email):
            raise Exception("Invalid Email")
        url = QIWIWalletURLS.receipt_email.format(txn_id)
        headers = {"Accept": "application/json",
                   "Content-type": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        json = {"email": email}
        params = {"type": type_operation.name}
        try:
            await Connector.request(url=url, headers=headers, json=json, params=params, request_type=POST,
                                    is_email=True)
        except ClientError:
            logger.warning(f"Cheque is not available (txnId: {txn_id}, type: {type_operation.name})")
        else:
            return True
        return False
