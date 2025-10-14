from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from uuid import uuid4
import pika


QUEUE_NAME = "pdf_queue"


executor = ProcessPoolExecutor(max_workers=4)


def slow_func():
    result = 0
    for x in range(10**9):
        result += x


def create_dir():
    output_dir = Path.cwd() / "output"
    path = output_dir.resolve()
    path.mkdir(exist_ok=True)
    return path


def process_message(content: bytes):
    print("Processing message in subprocess...")
    slow_func()
    file_path = create_dir() / f"{uuid4()}.txt"
    with file_path.open("wb") as file:
        file.write(content)
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
