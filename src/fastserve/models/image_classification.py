import logging
import os.path
import urllib
from typing import List

import torch
from fastapi import UploadFile
from pydantic import BaseModel

from fastserve import FastServe


class ResponseSchema(BaseModel):
    label: str
    score: float


class ServeImageClassification(FastServe):
    INPUT_SCHEMA = UploadFile

    def __init__(
        self, model_name: str, batch_size: int = 4, timeout: float = 0.2, device="cpu"
    ):
        super().__init__(
            batch_size=batch_size,
            timeout=timeout,
            input_schema=ServeImageClassification.INPUT_SCHEMA,
            response_schema=ResponseSchema,
        )
        import timm
        from timm.data import resolve_data_config
        from timm.data.transforms_factory import create_transform

        self.device = device
        self.model = timm.create_model(model_name, pretrained=True).to(device)
        self.model.eval()

        config = resolve_data_config({}, model=self.model)
        self.transform = create_transform(**config)

        if not os.path.isfile("imagenet_classes.txt"):
            logging.info("Downloading Imagenet classes")
            url, filename = (
                "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",
                "imagenet_classes.txt",
            )
            urllib.request.urlretrieve(url, filename)
        with open("imagenet_classes.txt") as f:
            self.categories = [s.strip() for s in f.readlines()]

    def process_image(self, filename):
        from PIL import Image

        img = Image.open(filename).convert("RGB")
        tensor = self.transform(img)  # transform and add batch dimension
        return tensor

    @torch.inference_mode()
    def handle(self, batch: List[UploadFile]) -> list[ResponseSchema]:
        tensors = []
        for file in batch:
            tensor = self.process_image(file.file)
            tensors.append(tensor)
        tensors = torch.stack(tensors).to(self.device)
        out = self.model(tensors)
        probs: torch.Tensor = torch.nn.functional.softmax(out, dim=1)  # batchX1000
        max_probs, indices = probs.max(1)  # batch x 1
        results = [
            ResponseSchema(label=self.categories[idx], score=p.cpu().item())
            for idx, p in zip(indices, max_probs)
        ]
        return results
