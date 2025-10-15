from pathlib import Path
import base64
import json


def slow_func():
    result = 0
    for x in range(10**8):
        result += x


def create_dir():
    output_dir = Path.cwd() / "output"
    path = output_dir.resolve()
    path.mkdir(exist_ok=True)
    return path


def wrap_data(file: bytes, metdata: dict):
    file_str = base64.b64encode(file).decode()
    metdata["file"] = file_str
    return json.dumps(metdata).encode()


def unwrap_data(data: bytes):
    data_dict = json.loads(data)
    file_bytes = base64.b64decode(data_dict["file"])
    del data_dict["file"]
    return file_bytes, data_dict
