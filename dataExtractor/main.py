from infrastructure.messaging.RabbitMQConsumer import RabbitMQConsumer

consumer = RabbitMQConsumer('frames')
consumer.start_consuming()
