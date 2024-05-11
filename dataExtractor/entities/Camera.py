from typing import Any

from geoalchemy2 import Geography
from sqlalchemy import Column, Integer, String, Numeric, Boolean, func
from shapely.geometry import Point
from geoalchemy2.shape import to_shape, from_shape


from .Base import Base


class Camera(Base):
    __tablename__ = 'cameras'

    def __init__(self, lat: float, lon: float, orient: float, name: str, source: str, **kw: Any):
        super().__init__(**kw)
        self.orientation = orient
        self.name = name
        self.source = source
        self.deleted = False
        self.set_location(lat, lon)

    def set_location(self, lat: float, lon: float):
        self.position = from_shape(Point(lat, lon), srid=4326)

    def get_location(self) -> Point:
        return to_shape(self.position)

    id = Column(Integer, primary_key=True)
    position = Column(Geography(geometry_type='POINT', srid=4326, spatial_index=False), nullable=False, unique=True)
    name = Column(String, nullable=False)
    source = Column(String, nullable=False, unique=True)
    orientation = Column(Numeric, nullable=False)
    deleted = Column(Boolean, nullable=False)
