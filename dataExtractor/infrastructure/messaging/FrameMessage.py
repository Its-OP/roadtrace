import json
from collections import defaultdict
from io import BytesIO
from typing import List, Dict

import cv2
import imageio
import msgpack
import numpy as np

from dtos.VehicleDto import VehicleDto
from entities import Region
from infrastructure.contracts.RegionContract import RegionContract


class FrameMessage:
    def __init__(self, packed_message: bytes):
        unpacked_data = msgpack.unpackb(packed_message, raw=False, strict_map_key=False)
        self.vehicles = self._unpack_results(unpacked_data)
        self.frames = dict(self._unpack_frames(unpacked_data))

    @staticmethod
    def _unpack_results(unpacked_data) -> List[VehicleDto]:
        vehicles: Dict[int, VehicleDto | None] = defaultdict(lambda: None)
        results: Dict[int, List[RegionContract]] = \
            { int(frame_id): [RegionContract(**json.loads(region_json)) for region_json in frame_regions]
              for frame_id, frame_regions in unpacked_data['results'].items() }

        for frame_id, regions in results.items():
            for region in regions:
                vehicle = vehicles[region.track_id]
                if vehicle is None:
                    vehicle = VehicleDto(str(region.track_id), [])
                    vehicles[region.track_id] = vehicle
                vehicle.regions.append(Region(region.x1, region.y1, region.x2, region.y2, frame_id))

        return list(vehicles.values())

    @staticmethod
    def _unpack_frames(unpacked_data) -> Dict[int, List[np.ndarray]]:
        frame_ids: List[int] = sorted([frame_id for frame_id, _ in unpacked_data['results'].items()])
        compressed_frames = unpacked_data['video']

        video_file_like = BytesIO(compressed_frames)

        # Use imageio to read the video
        reader = imageio.get_reader(video_file_like, format='mp4')

        # Initialize an empty list to hold the OpenCV-compatible images
        frames: List[np.ndarray] = []

        # Iterate over the frames
        for frame in reader:
            # Convert the frame to BGR color space (OpenCV uses BGR by default)
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Append the frame (now an OpenCV-compatible image) to the list
            frames.append(frame_bgr)

        return zip(frame_ids, frames)
