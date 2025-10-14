from celery import Celery


app = Celery(
    "pdf-generator",
    broker="amqp://guest:guest@rabbitmq:5672//",
    backend=None
)

app.autodiscover_tasks(["worker.tasks"])
