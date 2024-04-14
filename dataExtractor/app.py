import os
import keras

from sqlalchemy.orm import Session

import init_functions
from entities import Region, Vehicle
from infrastructure.database.db import UnitOfWork
from infrastructure.messaging.RabbitMQConsumer import RabbitMQConsumer
from services.ColorInferenceService import ColorInferenceService
from services.VmmrPredictorService import VmmrPredictorService

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

uow = UnitOfWork(POSTGRES_HOST)
uow.ensure_migrated()

with (uow.open_session() as session):
    session: Session
    session.query(Region).delete()
    session.query(Vehicle).delete()

color_picker: keras.Sequential = keras.models.load_model('models/color_picker.h5')
classes, model = init_functions.init_vmmr_predictor('models/vmmr_predictor.pt', 'models/vmmr_classes.pkl')

color_inf_service = ColorInferenceService(color_picker)
vmmr_predictor = VmmrPredictorService(model, classes)

consumer = RabbitMQConsumer('frames', uow, [color_inf_service, vmmr_predictor], RABBITMQ_HOST)
consumer.start_consuming()
