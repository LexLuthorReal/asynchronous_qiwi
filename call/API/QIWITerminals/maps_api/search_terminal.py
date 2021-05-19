from .....data.URL import QIWITerminals
from typing import Optional, List, Set
from .....models.QIWITerminals import SearchTerminal
from .....connector.aiohttp_connector import Connector
from .....data_types.connector.request_type import GET
from .....data_types.QIWITerminals import IdentificationMethods


class SearchTerminalsAPI:

    @classmethod
    async def search_terminals(cls, latitude_nw: float, longitude_nw: float, latitude_se: float, longitude_se: float,
                               zoom: Optional[int] = None, active_within_minutes: Optional[float] = None,
                               with_refill_wallet: Optional[bool] = None, ttp_ids: Optional[List[Set[int]]] = None,
                               cash_allowed: Optional[bool] = None, card_allowed: Optional[bool] = None,
                               identification_types: Optional[List[Set[IdentificationMethods]]] = None,
                               ttp_groups: Optional[List[Set[int]]] = None) -> dict:
        url = QIWITerminals.search_coordinates
        headers = {"Accept": "application/json"}
        if ttp_ids is not None:
            ttp_ids = list(ttp_ids[0])
        if identification_types is not None:
            identification_types = list(identification_types[0])
        if ttp_groups is not None:
            ttp_groups = list(ttp_groups[0])
        params = SearchTerminal(latNW=latitude_nw,
                                lngNW=longitude_nw,
                                latSE=latitude_se,
                                lngSE=longitude_se,
                                zoom=zoom,
                                activeWithinMinutes=active_within_minutes,
                                withRefillWallet=with_refill_wallet,
                                ttpIds=ttp_ids,
                                cacheAllowed=cash_allowed,
                                cardAllowed=card_allowed,
                                identificationTypes=identification_types,
                                ttpGroups=ttp_groups)
        response = await Connector.request(url=url,
                                           headers=headers,
                                           params=params.dict(by_alias=True, exclude_none=True),
                                           request_type=GET)
        response_data = await response.json()
        return response_data
