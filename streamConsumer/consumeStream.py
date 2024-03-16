import os
from typing import List

import cv2
import torch
import ultralytics

from Application.FrameProcessingResults import FrameProcessingResult
from Infrastructure.VideoEditor import VideoEditor
from Application.VideoProcessor import VideoProcessor

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Read env variables
VEHICLE_CODES = [int(x) for x in os.environ['VEHICLE_CODES'].split(',')]
TAKE_VIDEO_FROM = os.environ['TAKE_VIDEO_FROM']
EXPORT_FRAMES_TO = os.environ['EXPORT_FRAMES_TO']

# load models
model = ultralytics.YOLO('Artifacts/models/yolov8s.pt')
model.to(device)

# prepare to process video
cap = cv2.VideoCapture(TAKE_VIDEO_FROM)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

duration = frame_count / fps
file_size = file_size_bytes = os.path.getsize(TAKE_VIDEO_FROM)
bitrate = (file_size_bytes * 8) / duration

print("Total frames: " + str(frame_count))
video_editor = VideoEditor((frame_w, frame_h), (1920, 1088), fps)


def on_batch_processed(results: List[FrameProcessingResult]) -> None:
    raw_frames = [result.frame for result in results]
    bytes = video_editor.compress(raw_frames)
    # with open(EXPORT_FRAMES_TO, 'wb') as file:
    #     file.write(bytes)
    # sz = len(bytes)
    # a = 1


video_processor = VideoProcessor(model, 30, on_batch_processed, VEHICLE_CODES, 0.5, video_editor)
video_processor.start_processing(cap)

# frame_repository.export(EXPORT_FRAMES_TO)
