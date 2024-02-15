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
