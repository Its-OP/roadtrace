from abc import ABC, abstractmethod
from typing import List
from Application.Region import Region


class IVehicleDetector(ABC):
    @abstractmethod
    def detect_vehicles(self, regions: List[Region]) -> List[Region]:
        pass
