import logging
import time
import traceback
from typing import List

import pika
from pika.adapters.blocking_connection import BlockingConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
from pika.exceptions import AMQPConnectionError
from sqlalchemy.orm import Session

from infrastructure.database.db import UnitOfWork
from infrastructure.database.models import Vehicle, Region
from infrastructure.messaging.FrameMessage import FrameMessage
from services.BaseService import BaseService


class RabbitMQConsumer:
    def __init__(self, queue_name: str, uow: UnitOfWork, services: List[BaseService], host='localhost'):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self._uow = uow
        self._host = host
        self._services = services
        logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

    def _setup_channel(self):
        # Establish a connection with RabbitMQ server
        credentials = PlainCredentials('user', 'password')
        parameters = pika.ConnectionParameters(self._host, credentials=credentials)
        try:
            self.connection = self._create_connection_with_retry(parameters)
            if self.connection is None:
                raise AMQPConnectionError()

            self.channel = self.connection.channel()

            # Declare a queue
            self.channel.queue_declare(queue=self.queue_name)

            # Don't dispatch a new message to a worker until it has processed and acknowledged the previous one
            self.channel.basic_qos(prefetch_count=1)

            # Set up subscription on the queue with the provided callback
            self.channel.basic_consume(queue=self.queue_name,
                                       on_message_callback=self._callback,
                                       auto_ack=False)
        except AMQPConnectionError as conn_error:
            logging.error(f"Failed to establish a connection to host {self._host}: {conn_error}")
            print(traceback.format_exc())
            if self.connection and self.connection.is_open:
                self.connection.close()

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

            for service in self._services:
                service.process()

        print(f'Received {len(body)} bytes from {method.delivery_tag}')
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def _create_connection_with_retry(self,
                                     connection_parameters: ConnectionParameters,
                                     max_retries=5,
                                     initial_wait=1.0,
                                     backoff_factor=2) -> BlockingConnection | None:
        """
        Attempts to create a Pika blocking connection with exponential backoff.

        Parameters:
        - max_retries: Maximum number of retry attempts.
        - initial_wait: Initial wait time in seconds before retrying after the first failure.
        - backoff_factor: Factor by which the wait time increases after each failure.

        Returns:
        - A pika blocking connection if successful, None otherwise.
        """
        attempt = 0
        wait_time = initial_wait

        while attempt < max_retries:
            try:
                # Attempt to establish the connection
                connection = pika.BlockingConnection(connection_parameters)
                logging.info(f"Successfully connected to RabbitMQ on attempt {attempt+1}")
                return connection
            except pika.exceptions.AMQPConnectionError as e:
                logging.warning(f"Connection attempt {attempt+1} failed with error {e}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                attempt += 1
                wait_time *= backoff_factor  # Increase the wait time exponentially

        logging.error("Failed to connect to RabbitMQ after max retries.")
        return None

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