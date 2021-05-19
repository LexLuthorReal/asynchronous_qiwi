from typing import List, Set, Optional
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....utils.tools.datetime_str import DatetimeModule
from .....data_types.QIWIWallet import PaymentTypes, PaymentSources, DateRange


class StatisticPaymentsAPI:

    @staticmethod
    async def get_statistic_payments(wallet_api_key: str, phone_number: str, date_range: DateRange,
                                     operation_type: Optional[PaymentTypes] = None,
                                     sources_type: Optional[List[Set[PaymentSources]]] = None) -> dict:
        url = QIWIWalletURLS.statistic.format(phone_number)
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"startDate": await DatetimeModule.parse_datetime(date_range.start_date),
                  "endDate": await DatetimeModule.parse_datetime(date_range.end_date)}
        if operation_type is not None:
            params["operation"] = operation_type.name
        if sources_type is not None:
            for i, src_type in enumerate(sources_type[0]):
                params[f"sources[{i}]"] = src_type.name
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        return response_data
