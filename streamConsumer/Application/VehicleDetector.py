import numpy as np
from typing import List

from Application.Region import Region

VehicleCoordinates = np.ndarray


class VehicleDetector:
    def __init__(self, vehicle_codes: List[int], score_threshold: float):
        self._score_threshold = score_threshold
        self._vehicle_codes = vehicle_codes

    def filter_regions(self, possible_vehicle_regions: List[Region]) -> List[Region]:
        return [region for region in possible_vehicle_regions
                if region.class_id in self._vehicle_codes and region.score >= self._score_threshold]
