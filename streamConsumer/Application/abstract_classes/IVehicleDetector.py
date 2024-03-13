from abc import ABC, abstractmethod
from typing import List

import cv2

from Application.Region import Region


class IVehicleDetector(ABC):
    @abstractmethod
    def detect_vehicles(self, regions: List[Region]) -> List[Region]:
        pass
