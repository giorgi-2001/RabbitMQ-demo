import pika
from consumer import QUEUE_NAME


def send_pika_message(message: bytes):
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq",
            port=5672,
            credentials=credentials
        )
    )
    try:
        channel = connection.channel()
        channel.queue_declare(QUEUE_NAME, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key='pdf_queue',
            body=message
        )
    finally:
        connection.close()
