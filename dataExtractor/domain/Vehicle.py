from typing import List

from domain.Region import Region


class Vehicle:
    def __init__(self, local_tracking_id: str,
                 regions: List[Region],
                 color: str | None = None,
                 model: str | None = None,
                 state: str | None = None,
                 id: int | None = None):
        self._id: int = id
        self._local_tracking_id: str = local_tracking_id
        self._regions: List[Region] = regions
        self._color: str | None = color
        self._model: str | None = model
        self._state: str | None = state

    @property
    def id(self) -> int:
        return self._id

    @property
    def local_tracking_id(self) -> str:
        return self._local_tracking_id

    @property
    def regions(self) -> List[Region]:
        return self._regions

    @property
    def color(self) -> str | None:
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def model(self) -> str | None:
        return self._model

    @property
    def state(self) -> str | None:
        return self._state
