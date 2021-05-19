from typing import Optional, List, Set
from ..data_types.QIWITerminals import (
    IdentificationMethods
)
from .API.QIWITerminals import (
    TTPGroupsAPI,
    SearchTerminalsAPI
)
from ..models.QIWITerminals import (
    PartnerResult,
    TerminalResult
)


class Terminals:

    @staticmethod
    async def get_ttp_groups() -> PartnerResult:
        response_data = await TTPGroupsAPI.get_ttp_groups()
        return PartnerResult(result=response_data)

    @staticmethod
    async def search_terminals(latitude_nw: float, longitude_nw: float, latitude_se: float, longitude_se: float,
                               zoom: Optional[int] = None, active_within_minutes: Optional[float] = None,
                               with_refill_wallet: Optional[bool] = None, ttp_ids: Optional[List[Set[int]]] = None,
                               cash_allowed: Optional[bool] = None, card_allowed: Optional[bool] = None,
                               identification_types: Optional[List[Set[IdentificationMethods]]] = None,
                               ttp_groups: Optional[List[Set[int]]] = None) -> TerminalResult:
        response_data = await SearchTerminalsAPI.search_terminals(latitude_nw=latitude_nw,
                                                                  longitude_nw=longitude_nw,
                                                                  latitude_se=latitude_se,
                                                                  longitude_se=longitude_se,
                                                                  zoom=zoom,
                                                                  active_within_minutes=active_within_minutes,
                                                                  with_refill_wallet=with_refill_wallet,
                                                                  ttp_ids=ttp_ids,
                                                                  cash_allowed=cash_allowed,
                                                                  card_allowed=card_allowed,
                                                                  identification_types=identification_types,
                                                                  ttp_groups=ttp_groups)
        return TerminalResult(result=response_data)
