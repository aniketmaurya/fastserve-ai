from typing import Any

import torch
from pydantic import BaseModel


def get_default_device():
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class BaseRequest(BaseModel):
    request: Any
