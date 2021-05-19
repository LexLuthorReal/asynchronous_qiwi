from typing import Optional
from .....data.URL import QIWIWalletURLS
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....utils.tools.datetime_str import DatetimeModule
from .....data_types.QIWIWallet import InvoicesTypes, DateRange


class InvoiceStatementsAPI:

    @classmethod
    async def get_invoice_statements(cls, wallet_api_key: str, rows: Optional[int] = None, data_type: str = "CREATED",
                                     date_range: Optional[DateRange] = None, status: Optional[InvoicesTypes] = None,
                                     all_invoices: bool = False) -> dict:
        url = QIWIWalletURLS.Invoice.invoice_statements
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"dataType": data_type}
        if date_range is not None:
            params["startDateTime"] = await DatetimeModule.parse_datetime_p2p(dt=date_range.start_date)
            params["endDateTime"] = await DatetimeModule.parse_datetime_p2p(dt=date_range.end_date)
        if rows is not None:
            params["rows"] = rows
        if status is not None:
            params["statuses"] = status.name
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        if all_invoices:
            if response_data["result"]["nextInvoiceDate"] is not None:
                params["endDateTime"] = response_data["result"]["nextInvoiceDate"]
                while params["endDateTime"] is not None and params["endDateTime"] not in "1970-01-01T00:00:00.000Z":
                    # Get next history transactions data
                    response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
                    # Convert to the dict for work
                    response = await response.json()
                    # Set next invoice date
                    params["endDateTime"] = response["result"]["nextInvoiceDate"]
                    # Append to response data
                    response_data["result"]["nextInvoiceDate"] = response["result"]["nextInvoiceDate"]
                    # Get previous transaction
                    previous_list = response_data["result"]["invoices"]
                    # Append transaction
                    for invoice in response["result"]["invoices"]:
                        previous_list.append(invoice)
                    # Set "Appended" list
                    response_data["result"]["invoices"] = previous_list
                response_data["result"]["nextInvoiceDate"] = None
        return response_data
