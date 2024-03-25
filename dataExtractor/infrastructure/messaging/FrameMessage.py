from collections import defaultdict
from typing import List, Dict

import msgpack

from domain.Region import Region
from domain.Vehicle import Vehicle
from infrastructure.contracts.RegionContract import RegionContract


class FrameMessage:
    def __init__(self, packed_message: bytes):
        self.vehicles: List[Vehicle] = self._unpack_message(packed_message)

    @staticmethod
    def _unpack_message(body: bytes) -> List[Vehicle]:
        vehicles: Dict[int, Vehicle | None] = defaultdict(lambda: None)
        results: Dict[int, List[RegionContract]] = \
            { int(frame_id): [RegionContract(**region) for region in frame_regions]
              for frame_id, frame_regions in msgpack.unpackb(body, raw=False, strict_map_key=False)['results'].items() }

        for frame_id, regions in results.items():
            for region in regions:
                vehicle = vehicles[region.track_id]
                if vehicle is None:
                    vehicle = Vehicle(str(region.track_id), [])
                    vehicles[region.track_id] = vehicle
                vehicle.regions.append(Region(region.x1, region.y1, region.x2, region.y2, frame_id))

        return list(vehicles.values())
