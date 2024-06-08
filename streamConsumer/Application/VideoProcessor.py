import math
from typing import Callable, List, Tuple

import cv2
import numpy as np
import ultralytics
from ultralytics import YOLO

from Application.entities.FrameProcessingResultLight import FrameProcessingResultLight
from Application.entities.FrameProcessingResultRich import FrameProcessingResultRich
from Application.entities.Region import Region
from Application.Timer import Timer
from Application.interfaces.IRescaler import IRescaler
from Domain.Vehicle import Vehicle
from Domain.abstract_classes.IVideoProcessor import IVideoProcessor


class VideoProcessor(IVideoProcessor):
    def __init__(self,
                 model: YOLO,
                 max_batch_size: int,
                 on_frame_processed: Callable[[FrameProcessingResultLight], None],
                 on_batch_processed: Callable[[List[FrameProcessingResultRich]], None],
                 vehicle_codes: List[int],
                 detection_confidence_threshold: float,
                 video_editor: IRescaler):
        self._model = model
        self._video_editor = video_editor
        self._max_batch_size = max_batch_size
        self._on_frame_processed = on_frame_processed
        self._on_batch_processed = on_batch_processed
        self.detection_confidence_threshold = detection_confidence_threshold
        self._vehicle_codes = vehicle_codes
        self._processing_results: List[FrameProcessingResultRich] = []

    def start_processing(self, cap: cv2.VideoCapture):
        ret, frame = cap.read()
        frame = self._video_editor.rescale(frame)
        frame_nmr = 1
        with Timer('Stream was processed'):
            while ret or frame_nmr == 0:
                frame = self._video_editor.rescale(frame)
                with Timer(f"Regions of interest on frame {frame_nmr} were found and tracked"):
                    regions_of_interest = self._find_regions(frame)
    
                vehicles = [Vehicle(x1, y1, x2, y2, track_id) for (x1, y1, x2, y2, score, class_id, track_id)
                            in self._find_vehicles(regions_of_interest)]
                results = FrameProcessingResultRich(frame_nmr, vehicles, frame)
                self._on_frame_processed(results)
                self._processing_results.append(FrameProcessingResultRich(frame_nmr, vehicles, frame))
    
                if len(self._processing_results) >= self._max_batch_size:
                    self._refresh_batch()
    
                ret, frame = cap.read()
                frame_nmr += 1
    
            self._refresh_batch()
        print("Processing finished, shutting down...")

    def _find_regions(self, frame: np.ndarray) -> List[Region]:
        results: List[ultralytics.engine.results.Results]\
            = self._model.track(source=frame,
                                persist=True,
                                tracker="bytetrack.yaml",
                                imgsz=(self._normalize(frame.shape[0]),self._normalize(frame.shape[1])),
                                classes=self._vehicle_codes)
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
            with Timer("Callback executed"):
                self._on_batch_processed(self._processing_results)
            self._processing_results = []

    def _normalize(self, size: int) -> int:
        return math.ceil(size / 64) * 32
