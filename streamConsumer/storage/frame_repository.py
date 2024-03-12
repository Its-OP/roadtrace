import json
from typing import Dict, List

from entities.Vehicle import Vehicle
from storage.serialization_settings import serialize_complex_obj


class FrameRepository:
    def __init__(self):
        self._storage: Dict[int, Dict[int, Vehicle]] = {}

    def append_frame_info(self, frame_number: int, vehicles: List[Vehicle]):
        vehicles_dict = {vehicle.track_id: vehicle for vehicle in vehicles}
        self._storage[frame_number] = vehicles_dict

    def export(self, filepath: str):
        with open(filepath, 'w') as file:
            # Serialize dict and write it to the file
            json.dump(self._storage, file, default=serialize_complex_obj, indent=4)