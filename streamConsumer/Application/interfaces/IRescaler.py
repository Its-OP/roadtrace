from abc import ABC, abstractmethod

import numpy as np


class IRescaler(ABC):
    @abstractmethod
    def rescale(self, frame: np.ndarray) -> np.ndarray:
        pass
