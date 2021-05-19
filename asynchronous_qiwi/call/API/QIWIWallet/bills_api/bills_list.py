from typing import Optional
from .....data.URL import QIWIWalletURLS
from .....data_types.QIWIWallet import InvoicesTypes
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class BillsListAPI:

    @staticmethod
    async def get_list_of_bills(wallet_api_key: str, status: InvoicesTypes, rows: Optional[int] = None,
                                next_id: Optional[int] = None, all_bills: bool = False) -> dict:
        url = QIWIWalletURLS.Bills.list_bills
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {wallet_api_key}"}
        params = {"statuses": status.name}
        if rows is not None:
            params["rows"] = rows
        if next_id is not None:
            params["next_id"] = next_id
        response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
        response_data = await response.json()
        if all_bills:
            # Get length for bills
            len_bills = len(response_data["bills"])
            if len_bills > 0:
                # Set next bill for params
                params["next_id"] = response_data["bills"][len_bills - 1]["id"]
                while params["next_id"] is not None:
                    # Get next history transactions data
                    response = await Connector.request(url=url, headers=headers, params=params, request_type=GET)
                    # Convert to the dict for work
                    response = await response.json()
                    # Get length new bills
                    len_bills = len(response["bills"])
                    if len_bills > 0:
                        if response["bills"][0]["id"] == params["next_id"] and len_bills == 1:
                            params["next_id"] = None
                        else:
                            # Set next bill & Append to response data
                            params["next_id"] = response["bills"][len_bills - 1]["id"]
                            # Get previous transaction
                            previous_list = response_data["bills"]
                            # Remove first element
                            if response["bills"][0]["id"] == params["next_id"]:
                                del response["bills"][0]
                            # Append transaction
                            for bill in response["bills"]:
                                previous_list.append(bill)
                            # Set "Appended" list
                            response_data["bills"] = previous_list
                    else:
                        params["next_id"] = None
                response_data["next_bill_id"] = None
                response_data["next_bill_creation_datetime"] = None
        print(response_data)
        return response_data
