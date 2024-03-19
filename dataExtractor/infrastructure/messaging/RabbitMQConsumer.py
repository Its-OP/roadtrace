import pika
from pika.credentials import PlainCredentials


class RabbitMQConsumer:
    def __init__(self, queue_name: str):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

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