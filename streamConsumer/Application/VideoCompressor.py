import av
import numpy as np
from io import BytesIO
from typing import Tuple, List


# noinspection PyUnresolvedReferences
class VideoCompressor:
    def __init__(self, frame_dim: Tuple[int, int], frame_rate: int):
        self._frame_dim = frame_dim
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
