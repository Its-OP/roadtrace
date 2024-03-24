class Region:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

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
