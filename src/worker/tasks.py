from uuid import uuid4
from typing import cast
from celery import Task
from .celery import app

from .utils import create_dir, slow_func


@app.task
def generate_pdf(content: bytes):
    slow_func()
    file_path = create_dir() / f"{uuid4()}.pdf"
    with file_path.open("wb") as file:
        file.write(content)


generate_pdf_task = cast(Task, generate_pdf)
