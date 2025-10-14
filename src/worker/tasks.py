from uuid import uuid4
from pathlib import Path
from typing import cast
from celery import Task
from .celery import app


def create_dir():
    output_dir = Path.cwd() / "output"
    path = output_dir.resolve()
    path.mkdir(exist_ok=True)
    return path


def slow_func():
    result = 0
    for x in range(10**8):
        result += x


@app.task
def generate_pdf(content: bytes):
    slow_func()
    file_path = create_dir() / f"{uuid4()}.txt"
    with file_path.open("wb") as file:
        file.write(content)


generate_pdf_task = cast(Task, generate_pdf)
