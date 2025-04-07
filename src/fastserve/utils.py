import os
from typing import Any

from pydantic import BaseModel


def get_default_device():
    import torch

    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class BaseRequest(BaseModel):
    request: Any


def get_ui_folder():
    """Fetch the path to the UI folder from the installed package"""
    path = os.path.join(os.path.dirname(__file__), "../ui")
    path = os.path.abspath(path)
    return path


def download_file(url: str, dest: str):
    import requests
    from tqdm import tqdm

    if dest is None:
        dest = os.path.abspath(os.path.basename(dest))

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024
    with (
        open(dest, "wb") as file,
        tqdm(
            desc=dest,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar,
    ):
        for data in response.iter_content(block_size):
            file.write(data)
            bar.update(len(data))
    return dest
