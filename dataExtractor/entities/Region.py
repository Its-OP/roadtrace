from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey

from .Base import Base


class Region(Base):
    __tablename__ = 'regions'

    def __init__(self, x1: int, y1: int, x2: int, y2: int, frame_id: int, **kw: Any):
        super().__init__(**kw)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.frame_id = frame_id

    id = Column(Integer, primary_key=True)
    x1 = Column(Integer, nullable=False)
    y1 = Column(Integer, nullable=False)
    x2 = Column(Integer, nullable=False)
    y2 = Column(Integer, nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    frame_id = Column(String, nullable=False)
