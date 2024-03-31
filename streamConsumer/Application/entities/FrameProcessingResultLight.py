import json
from dataclasses import dataclass
from typing import List
from Domain.Vehicle import Vehicle


@dataclass
class FrameProcessingResultLight:
    frame_number: int
    vehicles: List[Vehicle]

    def __post_init__(self):
        self.vehicles_compacted = [json.dumps({ 'x1': v.x1, 'y1': v.y1, 'x2': v.x2, 'y2': v.y2, 'track_id': v.track_id })
                                   for v in self.vehicles]
