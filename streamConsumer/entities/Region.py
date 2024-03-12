from typing import NamedTuple


class Region(NamedTuple):
    x_min: int
    y_min: int
    x_max: int
    y_max: int
    score: float
    class_id: int
    track_id: int
