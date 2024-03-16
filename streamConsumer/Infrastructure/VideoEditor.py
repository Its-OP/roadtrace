import av
import cv2
import numpy as np
from io import BytesIO
from typing import Tuple, List

from Application.interfaces.IRescaler import IRescaler


class VideoEditor(IRescaler):
    def __init__(self, external_frame_dim: Tuple[int, int],
                 max_dim: Tuple[int, int],
                 frame_rate: int):
        self._frame_dim = self._calculate_frame_dimensions(max_dim, external_frame_dim)
        self._frame_rate = frame_rate
        self._video_format = 'mp4'
        self._codec = 'libx264'
        self._frame_pixel_format = 'bgr24'
        self._video_pixel_format = 'yuv420p'

    def compress(self, frames: List[np.ndarray]) -> bytes:
        output_buffer = BytesIO()

        output_container: av.container.output.OutputContainer
        with av.open(output_buffer, mode='w', format=self._video_format) as output_container:
            # Add a video stream to the container, specifying codec and other parameters
            video_stream: av.video.stream.VideoStream = output_container.add_stream(self._codec, self._frame_rate)
            video_stream.width = self._frame_dim[0]
            video_stream.height = self._frame_dim[1]
            video_stream.pix_fmt = self._video_pixel_format
            video_stream.options = { 'crf': str(25), 'preset': 'ultrafast' }

            for frame in frames:
                # Create a new frame for the video stream
                av_frame = av.VideoFrame.from_ndarray(frame, format=self._frame_pixel_format)

                # Convert the frame to the required pixel format
                av_frame = av_frame.reformat(video_stream.width, video_stream.height, video_stream.pix_fmt)

                # Encode the frame
                for packet in video_stream.encode(av_frame):
                    output_container.mux(packet)

            # Finalize the stream by encoding any buffered frames
            for packet in video_stream.encode():
                output_container.mux(packet)

        # Return the bytes
        return output_buffer.getvalue()

    def rescale(self, frame: np.ndarray) -> np.ndarray:
        return cv2.resize(frame, self._frame_dim, interpolation=cv2.INTER_AREA)

    @staticmethod
    def _calculate_frame_dimensions(max_dim: Tuple[int, int], frame_dim: Tuple[int, int]) -> Tuple[int, int]:
        scale_w = min(max_dim[0] / frame_dim[0], 1)
        scale_h = min(max_dim[1] / frame_dim[1], 1)
        # Use the smaller scale factor to preserve aspect ratio
        scale = min(scale_w, scale_h)

        # Calculate new dimensions
        new_w = int(frame_dim[0] * scale)
        new_h = int(frame_dim[1] * scale)

        # Adjust dimensions to be divisible by 32
        new_w = new_w - (new_w % 32)
        new_h = new_h - (new_h % 32)
        return new_w, new_h
