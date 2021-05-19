from typing import List, Set, Optional
from .....data.URL import QIWIWalletURLS
from .....models.QIWIWallet import NextPayment
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....utils.tools.datetime_str import DatetimeModule
from .....data_types.QIWIWallet import PaymentTypes, PaymentSources, DateRange


class HistoryPaymentsAPI:

    @staticmethod
    async def get_history(wallet_api_key: str, phone_number: str, rows: int = 50,
                          operation_type: Optional[PaymentTypes] = None,
                          sources_type: Optional[List[Set[PaymentSources]]] = None,
                          date_range: Optional[DateRange] = None, next_txn: Optional[NextPayment] = None,
                          all_transactions: bool = False) -> dict:
        url = QIWIWalletURLS.history.format(phone_number)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"rows": rows}
        if operation_type is not None:
            params["operation"] = operation_type.name
        if sources_type is not None:
            for i, src_type in enumerate(sources_type[0]):
                params[f"sources[{i}]"] = src_type.name
        if date_range is not None:
            params["startDate"] = await DatetimeModule.parse_datetime(date_range.start_date)
            params["endDate"] = await DatetimeModule.parse_datetime(date_range.end_date)
        if next_txn is not None:
            params["nextTxnId"] = next_txn.next_txn_id
            params["nextTxnDate"] = await DatetimeModule.parse_datetime(next_txn.next_txn_date)
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        if all_transactions:
            # Set next transaction for params
            params["nextTxnId"], params["nextTxnDate"] = response_data["nextTxnId"], response_data["nextTxnDate"]
            while params["nextTxnId"] is not None and params["nextTxnDate"] is not None:
                # Get next history transactions data
                response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
                # Convert to the dict for work
                response = await response.json()
                # Set next transactions & Append to response data
                params["nextTxnId"], response_data["nextTxnId"] = response["nextTxnId"], response["nextTxnId"]
                params["nextTxnDate"], response_data["nextTxnDate"] = response["nextTxnDate"], response["nextTxnDate"]
                # Get previous transaction
                previous_list = response_data["data"]
                # Append transaction
                for transaction in response["data"]:
                    previous_list.append(transaction)
                # Set "Appended" list
                response_data["data"] = previous_list
        return response_data
