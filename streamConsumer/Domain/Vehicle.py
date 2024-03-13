class Vehicle:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, track_id: int):
        # Basic validation to ensure that x1 < x2 and y1 < y2
        if x2 <= x1 or y2 <= y1:
            raise ValueError("Coordinates are not valid. Ensure that x1 < x2 and y1 < y2.")

        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2
        self._track_id = track_id

    # Getters
    @property
    def x1(self) -> int:
        return self._x1

    @property
    def y1(self) -> int:
        return self._y1

    @property
    def x2(self) -> int:
        return self._x2

    @property
    def y2(self) -> int:
        return self._y2

    @property
    def track_id(self) -> int:
        return self._track_id
