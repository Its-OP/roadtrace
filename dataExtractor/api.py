import os
from typing import List, cast

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import entities
import schemas
from infrastructure.database.db import UnitOfWork

app = FastAPI()

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
uow = UnitOfWork(POSTGRES_HOST)
uow.ensure_migrated()


def fetch_cameras(db: Session) -> List[schemas.Camera]:
    return [schemas.Camera.from_domain(camera) for camera in db.query(entities.Camera).filter_by(
        deleted=False
    ).all()]


@app.get("/cameras", response_model=List[schemas.Camera])
def get_cameras():
    with uow.open_session() as db:
        return fetch_cameras(db)


@app.post("/cameras", response_model=List[schemas.Camera])
def add_or_update_cameras(cameras: List[schemas.Camera]):
    with uow.open_session() as db:
        for camera in cameras:
            if camera.id != 0:
                domain_camera: entities.Camera = db.query(entities.Camera).filter_by(
                    id=camera.id, deleted=False
                ).one_or_none()
                if domain_camera is None or domain_camera.deleted is True:
                    continue

                domain_camera.name = camera.name
                domain_camera.source = camera.source
                domain_camera.orientation = camera.orientation
                domain_camera.set_location(camera.lat, camera.lon)
            else:
                domain_camera = entities.Camera(camera.lat, camera.lon, camera.orientation, camera.name, camera.source)
                db.add(domain_camera)

        return fetch_cameras(db)


@app.delete("/cameras/{camera_id}", response_model=List[schemas.Camera])
def delete_camera(camera_id: int):
    with uow.open_session() as db:
        domain_camera: entities.Camera = db.query(entities.Camera).filter_by(
            id=camera_id, deleted=False
        ).one_or_none()

        if domain_camera is not None:
            domain_camera.deleted = True

        return fetch_cameras(db)
