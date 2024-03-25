import pika
from pika.credentials import PlainCredentials
from sqlalchemy.orm import Session

from infrastructure.database.db import UnitOfWork
from infrastructure.database.models import Vehicle, Region
from infrastructure.messaging.FrameMessage import FrameMessage


class RabbitMQConsumer:
    def __init__(self, queue_name: str, uow: UnitOfWork):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self._uow = uow

    def _setup_channel(self):
        # Establish a connection with RabbitMQ server
        credentials = PlainCredentials('user', 'password')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', credentials=credentials))
        self.channel = self.connection.channel()

        # Declare a queue
        self.channel.queue_declare(queue=self.queue_name)

        # Don't dispatch a new message to a worker until it has processed and acknowledged the previous one
        self.channel.basic_qos(prefetch_count=1)

        # Set up subscription on the queue with the provided callback
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self._callback,
                                   auto_ack=False)

    def _callback(self, ch: pika.channel.Channel, method: pika.spec.Basic.Deliver,
                  properties: pika.spec.BasicProperties, body: bytes):
        with (self._uow.open_session() as session):
            session: Session
            frame_message = FrameMessage(body)
            for vehicle in frame_message.vehicles:
                model_vehicle = session.query(Vehicle
                                              ).filter(Vehicle.external_id == vehicle.local_tracking_id).one_or_none()
                model_regions = [Region.from_domain(region) for region in vehicle.regions]
                if model_vehicle is None:
                    model_vehicle = Vehicle.from_domain(vehicle)
                    session.add(model_vehicle)

                model_vehicle.regions.extend(model_regions)

        print(f'Received {len(body)} bytes from {method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        if not self.channel or self.channel.is_closed:
            self._setup_channel()

        print(f" [*] Waiting for messages from queue {self.queue_name}. To exit press CTRL+C")
        try:
            # Start consuming messages
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print(' [x] Consumer stopped.')
        finally:
            if self.connection and self.connection.is_open:
                self.connection.close()
                print(' [x] Connection closed.')