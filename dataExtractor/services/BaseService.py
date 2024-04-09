from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Generic

import numpy as np

from entities import Vehicle, Region

Frame = np.ndarray

TFeature = TypeVar('TFeature')


class BaseService(ABC, Generic[TFeature]):
    @abstractmethod
    def _should_process_vehicle(self, vehicle: Vehicle) -> bool:
        pass

    @abstractmethod
    def _preprocess_frame(self, frame: Frame) -> np.ndarray:
        pass

    @abstractmethod
    def _extract_feature(self, region: Region, preprocessed_frame: Frame) -> TFeature | None:
        pass

    @abstractmethod
    def _update_vehicle(self, vehicle: Vehicle, feature: TFeature):
        pass

    def process(self, vehicles: List[Vehicle], frames: Dict[int, Frame]) -> List[Vehicle]:
        for vehicle in vehicles:
            if not self._should_process_vehicle(vehicle):
                continue
            for region in vehicle.regions:
                sliced_frame = frames[region.frame_id][region.y1:region.y2, region.x1:region.x2]
                preprocessed_frame = self._preprocess_frame(sliced_frame)
                feature = self._extract_feature(region, preprocessed_frame)
                if feature is not None:
                    self._update_vehicle(vehicle, feature)
                    break

        return vehicles
