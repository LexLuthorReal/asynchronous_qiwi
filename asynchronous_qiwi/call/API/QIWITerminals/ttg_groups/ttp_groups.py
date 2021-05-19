from .....data.URL import QIWITerminals
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET


class TTPGroupsAPI(Connector):

    @classmethod
    async def get_ttp_groups(cls) -> dict:
        url = QIWITerminals.ttp_groups
        headers = {"Accept": "application/json"}
        response = await Connector.request(url=url, headers=headers, request_type=GET)
        response_data = await response.json()
        return response_data
