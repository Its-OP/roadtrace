from typing import NamedTuple, List

from entities import Region


class VehicleDto(NamedTuple):
    external_id: str
    regions: List[Region]
