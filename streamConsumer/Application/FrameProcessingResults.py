from typing import NamedTuple, List

from Domain.Vehicle import Vehicle


class FrameProcessingResult(NamedTuple):
    frame_number: int
    vehicles: List[Vehicle]
