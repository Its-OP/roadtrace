import os

from sqlalchemy.orm import Session

from infrastructure.database.db import UnitOfWork
from infrastructure.database.models import Vehicle, Region
from infrastructure.messaging.RabbitMQConsumer import RabbitMQConsumer

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

uow = UnitOfWork(POSTGRES_HOST)
uow.ensure_migrated()

with (uow.open_session() as session):
    session: Session
    session.query(Region).delete()
    session.query(Vehicle).delete()

consumer = RabbitMQConsumer('frames', uow, RABBITMQ_HOST)
consumer.start_consuming()
