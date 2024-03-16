from typing import NamedTuple, List

import numpy as np

from Domain.Vehicle import Vehicle


class FrameProcessingResult(NamedTuple):
    frame_number: int
    vehicles: List[Vehicle]
    frame: np.ndarray
