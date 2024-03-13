import os
from typing import List

import cv2
import torch
import ultralytics

from Application.FrameProcessingResults import FrameProcessingResult
from Application.VideoProcessor import VideoProcessor
from Infrastructure.frame_repository import FrameRepository

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Read env variables
VEHICLE_CODES = [int(x) for x in os.environ['VEHICLE_CODES'].split(',')]
TAKE_VIDEO_FROM = os.environ['TAKE_VIDEO_FROM']
EXPORT_FRAMES_TO = os.environ['EXPORT_FRAMES_TO']

# load models
model = ultralytics.YOLO('Artifacts/models/yolov8n.pt')
model.to(device)

# prepare to process video
cap = cv2.VideoCapture(TAKE_VIDEO_FROM)
print("Total frames: " + str(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
frame_repository = FrameRepository()


def on_batch_processed(results: List[FrameProcessingResult]) -> None:
    for result in results:
        frame_repository.append_frame_info(result.frame_number, result.vehicles)


video_processor = VideoProcessor(model, 30, on_batch_processed, VEHICLE_CODES, 0.5)
video_processor.start_processing(cap)

frame_repository.export(EXPORT_FRAMES_TO)
