from pydantic import BaseModel, Field

import entities


class Camera(BaseModel):
    id: int
    lat: float = Field(ge=-180, le=180)
    lon: float = Field(ge=-90, le=90)
    name: str
    source: str
    orientation: float = Field(ge=0, le=360)

    @staticmethod
    def from_domain(camera: entities.Camera) -> 'Camera':
        return Camera(id=camera.id,
                      lat=camera.get_location().y,
                      lon=camera.get_location().x,
                      name=camera.name,
                      source=camera.source,
                      orientation=camera.orientation)
