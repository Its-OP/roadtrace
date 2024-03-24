from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from domain.Vehicle import Vehicle as DomainVehicle

from .Base import Base


class Vehicle(Base):
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    external_id = Column(String, nullable=False, unique=True)
    color = Column(String, nullable=True)
    model = Column(String, nullable=True)
    state = Column(String, nullable=True)
    regions = relationship('Region', backref='vehicle', lazy=True)

    def to_domain(self) -> DomainVehicle:
        return DomainVehicle(self.external_id, self.color, self.model, self.state, self.regions, self.id)

    @staticmethod
    def from_domain(domain_vehicle: DomainVehicle):
        return Vehicle(id=domain_vehicle.id, external_id=domain_vehicle.local_tracking_id, color=domain_vehicle.color,
                       model=domain_vehicle.model, state=domain_vehicle.state, regions=domain_vehicle.regions)
