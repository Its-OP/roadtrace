from dataclasses import dataclass

import numpy as np
from Application.entities.FrameProcessingResultLight import FrameProcessingResultLight


@dataclass
class FrameProcessingResultRich(FrameProcessingResultLight):
    frame: np.ndarray
