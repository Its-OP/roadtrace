import logging
import queue

import pika
from pika.exceptions import AMQPError

from Application.interfaces.messaging.IMessagePublisher import IMessagePublisher


class RabbitMQPublisher(IMessagePublisher):
    def __init__(self, queue_name='frames', host='localhost'):
        super().__init__()
        self.queue_name = queue_name

        # Configure logging
        logging.basicConfig(level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

    def run(self) -> None:
        try:
            credentials = pika.PlainCredentials('user', 'password')
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
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
