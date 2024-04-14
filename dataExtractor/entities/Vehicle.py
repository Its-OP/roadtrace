from typing import List, Any

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import Region
from .Base import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    def __init__(self,
                 external_id: str,
                 regions: List[Region],
                 color: str | None = None,
                 model: str | None = None,
                 make: str | None = None,
                 id: int | None = None,
                 **kw: Any):
        super().__init__(**kw)
        self.id: int = id
        self.external_id: str = external_id
        self.color: str | None = color
        self.model: str | None = model
        self.make: str | None = make
        self.regions = regions

    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)
    model = Column(String, nullable=True)
    make = Column(String, nullable=True)
    regions = relationship('Region', backref='vehicle', lazy=True)
