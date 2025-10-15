from concurrent.futures import ProcessPoolExecutor
from uuid import uuid4
import pika

from worker.utils import create_dir, slow_func, unwrap_data


QUEUE_NAME = "pdf_queue"


executor = ProcessPoolExecutor(max_workers=4)


def process_message(content: bytes):
    print("Processing message in subprocess...")

    file_bytes, metadata = unwrap_data(content)
    print("File data recieved: ", metadata)

    slow_func()
    file_path = create_dir() / f"{uuid4()}.pdf"
    with file_path.open("wb") as file:
        file.write(file_bytes)
    print("File written successfully.")


def callback(ch, method, properties, content: bytes):
    executor.submit(process_message, content)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    print("Connecting to RabbitMQ")
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
        channel.basic_qos(prefetch_count=4)
        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interupted by user")
    except Exception as e:
        print("Error occures: ", e)
    finally:
        executor.shutdown(wait=True)
        connection.close()


if __name__ == "__main__":
    main()
