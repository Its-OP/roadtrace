from dataclasses import dataclass
from typing import List
from Domain.Vehicle import Vehicle


@dataclass(frozen=True)
class FrameProcessingResultLight:
    frame_number: int
    vehicles: List[Vehicle]
