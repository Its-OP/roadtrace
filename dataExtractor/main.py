from infrastructure.database.db import UnitOfWork
from infrastructure.messaging.RabbitMQConsumer import RabbitMQConsumer


uow = UnitOfWork()
uow.ensure_migrated()

consumer = RabbitMQConsumer('frames', uow)
consumer.start_consuming()
