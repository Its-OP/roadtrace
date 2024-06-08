import os
import time
from typing import List

import cv2
import torch
import ultralytics
from redis.client import Redis
from redis.exceptions import ResponseError

from Application.entities.FrameProcessingResultLight import FrameProcessingResultLight
from Application.entities.FrameProcessingResultRich import FrameProcessingResultRich
from Infrastructure.VideoEditor import VideoEditor
from Application.VideoProcessor import VideoProcessor
from Infrastructure.messaging.FrameMessage import FrameMessage
from Infrastructure.messaging.RabbitMQPublisher import RabbitMQPublisher

# Check for CUDA device and set it
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Read env variables
VEHICLE_CODES = [int(x) for x in os.environ['VEHICLE_CODES'].split(',')]
TAKE_VIDEO_FROM = os.environ['TAKE_VIDEO_FROM']
REDIS_HOST = os.environ['REDIS_HOST']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']

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

# init services
video_editor = VideoEditor((frame_w, frame_h), (1920, 1088), fps)
publisher = RabbitMQPublisher(host=RABBITMQ_HOST)

# init Redis
ts_conn = Redis(host=REDIS_HOST, port=6379, db=0)
rts_client = ts_conn.ts()
metadata_client = Redis(host=REDIS_HOST, port=6379, db=1)
rts_key_name = 'rts:cam1'
metadata_key_prefix = 'meta:cam1'

metadata_client.flushall()

try:
    # Attempt to create the time series
    rts_client.create(rts_key_name)
    print(f"Time series '{rts_key_name}' created successfully.")
except ResponseError as e:
    if "already exists" in str(e):
        print(f"Time series '{rts_key_name}' already exists, proceeding without creating.")
    else:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")


def on_frame_processed(result: FrameProcessingResultLight) -> None:
    rts_client.add(rts_key_name, '*', result.frame_number)
    metadata_client.lpush(f"{metadata_key_prefix}:{result.frame_number}", *result.vehicles_compacted)


def on_batch_processed(results: List[FrameProcessingResultRich]) -> None:
    raw_frames = [result.frame for result in results]
    # bytes = video_editor.compress(raw_frames)
    # message = FrameMessage(results, bytes)
    # publisher.send_message(message)


video_processor = VideoProcessor(model, 30, on_frame_processed, on_batch_processed, VEHICLE_CODES, 0.5, video_editor)
publisher.start()

video_processor.start_processing(cap)
