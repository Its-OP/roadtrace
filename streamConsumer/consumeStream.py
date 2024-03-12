import os
import sys
import time
from typing import List, Tuple

import torch

import ultralytics
import cv2

from entities.Region import Region
from entities.Vehicle import Vehicle

from services.VehicleDetector import VehicleDetector
from storage.frame_repository import FrameRepository

args = sys.argv

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Read env variables
VEHICLE_CODES = [int(x) for x in os.environ['VEHICLE_CODES'].split(',')]
TAKE_VIDEO_FROM = os.environ['TAKE_VIDEO_FROM']
EXPORT_FRAMES_TO = os.environ['EXPORT_FRAMES_TO']

# load models
model = ultralytics.YOLO('./models/yolov8n.pt')
model.to(device)

# load video
cap = cv2.VideoCapture(TAKE_VIDEO_FROM)
print("Total frames: " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

# read frames
frame_nmr = 0
holding_frames = []
ret = True

vehicle_detector = VehicleDetector(VEHICLE_CODES, 0.5)
frame_repository = FrameRepository()

while ret and frame_nmr < 30:
    start_time = time.time()
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        # detect and track regions
        start_detection_time = time.time()
        results: List[ultralytics.engine.results.Results] = model.track(frame, persist=True)
        boxes: List[Tuple[int]] = \
            [tuple(box_coordinates) for box_coordinates in results[0].boxes.xyxy.int().cpu().tolist()]
        scores: List[float] = results[0].boxes.conf.float().cpu().tolist()
        classes: List[int] = results[0].boxes.cls.int().cpu().tolist()
        track_ids: List[int] = results[0].boxes.id.int().cpu().tolist()

        regions = [Region(*t) for t
                   in [box + (score,) + (cls,) + (track_id,) for (box, score, cls, track_id)
                       in zip(boxes, scores, classes, track_ids)]]

        print(f"Vehicles on the frame {frame_nmr} were detected. Total detection + tracking time is:"
              f"{time.time() - start_detection_time} seconds")
        total_detections = model(frame)[0]

        regions_with_vehicles = vehicle_detector.filter_regions(regions)
        vehicles = [Vehicle(x1, y1, x2, y2, track_id) for (x1, y1, x2, y2, score, class_id, track_id)
                    in vehicle_detector.filter_regions(regions)]

        frame_repository.append_frame_info(frame_nmr, vehicles)
        print()

    end_time = time.time()
    print(f"Frame {frame_nmr} was processed. Total processing time is: {end_time - start_time} seconds")

print("Processing finished, shutting down...")

frame_repository.export(EXPORT_FRAMES_TO)
