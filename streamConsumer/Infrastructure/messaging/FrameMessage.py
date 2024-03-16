from typing import List

import msgpack

from Application.entities.FrameProcessingResultLight import FrameProcessingResultLight
from Application.interfaces.messaging.IMessage import IMessage


class FrameMessage(IMessage):
    def __init__(self, processing_results: List[FrameProcessingResultLight], compressed_frames: bytes):
        self._processing_results = processing_results
        self._compressed_frames = compressed_frames

    def pack(self) -> bytes:
        packed_message: bytes = msgpack.packb({
            'video': self._compressed_frames,
            'results': {
                r.frame_number: [{ 'x1': v.x1, 'y1': v.y1, 'x2': v.x2, 'y2': v.y2, 'track_id': v.track_id } for v in
                                 r.vehicles] for r in self._processing_results
            }
        })

        return packed_message
