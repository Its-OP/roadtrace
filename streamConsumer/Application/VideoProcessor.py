import time
from typing import Callable, List, Tuple

import cv2
import numpy as np
import ultralytics
from ultralytics import YOLO

from Application.FrameProcessingResults import FrameProcessingResult
from Application.Region import Region
from Domain.Vehicle import Vehicle
from Domain.abstract_classes.IVideoProcessor import IVideoProcessor


class VideoProcessor(IVideoProcessor):
    def __init__(self, model: YOLO, max_batch_size: int,
                 on_batch_processed: Callable[[List[FrameProcessingResult]], None],
                 vehicle_codes: List[int], detection_confidence_threshold: float):
        self._model = model
        self._max_batch_size = max_batch_size
        self._on_batch_processed = on_batch_processed
        self.detection_confidence_threshold = detection_confidence_threshold
        self._vehicle_codes = vehicle_codes
        self._processing_results: List[FrameProcessingResult] = []

    def start_processing(self, cap: cv2.VideoCapture):
        ret, frame = cap.read()
        frame_nmr = 1
        while ret or frame_nmr == 0:
            start_time = time.time()

            regions_of_interest = self._find_regions(frame)
            print(f"Regions of interest on frame {frame_nmr} were found and tracked detected. Time elapsed:"
                  f"{time.time() - start_time} seconds")

            vehicles = [Vehicle(x1, y1, x2, y2, track_id) for (x1, y1, x2, y2, score, class_id, track_id)
                        in self._find_vehicles(regions_of_interest)]
            self._processing_results.append(FrameProcessingResult(frame_nmr, vehicles))

            if len(self._processing_results) > self._max_batch_size:
                self._refresh_batch()

            ret, frame = cap.read()
            frame_nmr += 1

        self._refresh_batch()
        print("Processing finished, shutting down...")

    def _find_regions(self, frame: np.ndarray) -> List[Region]:
        results: List[ultralytics.engine.results.Results] = self._model.track(frame, persist=True)
        boxes: List[Tuple[int]] = \
            [tuple(box_coordinates) for box_coordinates in results[0].boxes.xyxy.int().cpu().tolist()]
        scores: List[float] = results[0].boxes.conf.float().cpu().tolist()
        classes: List[int] = results[0].boxes.cls.int().cpu().tolist()
        track_ids: List[int] = results[0].boxes.id.int().cpu().tolist()

        regions = [Region(*t) for t
                   in [box + (score,) + (cls,) + (track_id,) for (box, score, cls, track_id)
                       in zip(boxes, scores, classes, track_ids)]]
        return regions

    def _find_vehicles(self, regions_of_interest: List[Region]) -> List[Region]:
        return [region for region in regions_of_interest
                if region.class_id in self._vehicle_codes and region.score >= self.detection_confidence_threshold]

    def _refresh_batch(self):
        if self._processing_results:
            self._on_batch_processed(self._processing_results)
            self._processing_results = []
