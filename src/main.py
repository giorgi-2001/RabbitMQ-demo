from fastapi import FastAPI, Form, File, UploadFile
from typing import Annotated
from worker.tasks import generate_pdf_task
from publisher import send_pika_message


app = FastAPI()


@app.get("/", tags=["Index"])
def index():
    return {"message": "hello, world!"}


@app.post("/celery", tags=["Celery"])
async def generate_pdf_file_celery(
    file: Annotated[UploadFile, File()],
    copies: int = Form(1, ge=1, le=20)
):
    content = await file.read()
    for _ in range(copies):
        generate_pdf_task.delay(content)

    return {"message": f"your file - {file.filename} - was recieved"}


@app.post("/pika", tags=["Pika"])
async def generate_pdf_file_pika(
    file: Annotated[UploadFile, File()],
    copies: int = Form(1, ge=1, le=20)
):
    content = await file.read()
    for _ in range(copies):
        send_pika_message(content)

    return {"message": f"your file - {file.filename} - was recieved"}
