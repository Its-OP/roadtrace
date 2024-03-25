from sqlalchemy import Column, Integer, String, ForeignKey

from domain.Region import Region as DomainRegion
from .Base import Base


class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    x1 = Column(Integer, nullable=False)
    y1 = Column(Integer, nullable=False)
    x2 = Column(Integer, nullable=False)
    y2 = Column(Integer, nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    frame_id = Column(String, nullable=False)

    @property
    def vehicle(self):
        return self.vehicle

    def to_domain(self) -> DomainRegion:
        return DomainRegion(self.x1, self.y1, self.x2, self.y2)

    @staticmethod
    def from_domain(domain_region: DomainRegion):
        return Region(x1=domain_region.x1,
                      y1=domain_region.y1,
                      x2=domain_region.x2,
                      y2=domain_region.y2,
                      frame_id=domain_region.frame_id)
