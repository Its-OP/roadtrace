import logging
import queue
import time

import pika
from pika import ConnectionParameters, BlockingConnection
from pika.exceptions import AMQPError, AMQPConnectionError

from Application.interfaces.messaging.IMessagePublisher import IMessagePublisher


class RabbitMQPublisher(IMessagePublisher):
    def __init__(self, queue_name='frames', host='localhost'):
        super().__init__()
        self.queue_name = queue_name
        self._host = host

        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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
                logging.info(f"Successfully connected to RabbitMQ on attempt {attempt + 1}")
                return connection
            except pika.exceptions.AMQPConnectionError as e:
                logging.warning(f"Connection attempt {attempt + 1} failed. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                attempt += 1
                wait_time *= backoff_factor  # Increase the wait time exponentially

        logging.error("Failed to connect to RabbitMQ after max retries.")
        return None

    def run(self) -> None:
        try:
            credentials = pika.PlainCredentials('user', 'password')
            parameters = pika.ConnectionParameters(host=self._host, credentials=credentials)
            connection = self._create_connection_with_retry(parameters)
            if connection is None:
                raise AMQPConnectionError()

            channel = connection.channel()
            channel.queue_declare(queue=self.queue_name)

            while self._is_active:
                try:
                    message = self._message_queue.get(timeout=1)  # Adjust timeout as needed
                    body = message.pack()
                    channel.basic_publish(exchange='',
                                          routing_key=self.queue_name,
                                          body=body)
                    print("Message sent")
                except queue.Empty:
                    continue  # Timeout reached, loop again
                except AMQPError as amqp_error:
                    logging.error(f"AMQP error while sending message: {amqp_error}")
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
        except pika.exceptions.AMQPConnectionError as conn_error:
            logging.error(f"Failed to establish a connection: {conn_error}")
        finally:
            if connection and connection.is_open:
                connection.close()
