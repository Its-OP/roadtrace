from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Generic

import numpy as np

from domain.Region import Region
from domain.Vehicle import Vehicle
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
    def _extract_feature(self, region: Region, frame: Frame) -> TFeature | None:
        pass

    @abstractmethod
    def _update_vehicle(self, vehicle: Vehicle, feature: TFeature):
        pass

    def process(self, vehicles: List[Vehicle], frames: Dict[int, Frame]) -> List[Vehicle]:
        preprocessed_frames: Dict[int, Frame] = {}
        for vehicle in vehicles:
            if self._should_process_vehicle(vehicle):
                continue

            for region in vehicle.regions:
                preprocessed_frame: Frame
                if region.frame_id in preprocessed_frames:
                    preprocessed_frame = preprocessed_frames[region.frame_id]
                else:
                    preprocessed_frame = self._preprocess_frame(frames[region.frame_id])
                    preprocessed_frames[region.frame_id] = preprocessed_frame
                feature = self._extract_feature(region, preprocessed_frame)
                if feature is not None:
                    self._update_vehicle(vehicle, feature)
                    break

        return vehicles
