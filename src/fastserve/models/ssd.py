import io
from typing import List

import torch
from diffusers import StableDiffusionXLPipeline
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from fastserve import FastServe


class PromptRequest(BaseModel):
    prompt: str  # "An astronaut riding a green horse"
    negative_prompt: str = "ugly, blurry, poor quality"


class ServeSSD1B(FastServe):
    def __init__(
        self, batch_size=1, timeout=0.0, device="cuda", num_inference_steps: int = 50
    ) -> None:
        self.num_inference_steps = num_inference_steps
        self.input_schema = PromptRequest
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            "segmind/SSD-1B",
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.pipe.to(device)
        super().__init__(batch_size, timeout)

    def handle(self, batch: List[PromptRequest]) -> List[StreamingResponse]:
        prompts = [b.prompt for b in batch]
        negative_prompts = [b.negative_prompt for b in batch]

        pil_images = self.pipe(
            prompt=prompts,
            negative_prompt=negative_prompts,
            num_inference_steps=self.num_inference_steps,
        ).images
        image_bytes_list = []
        for pil_image in pil_images:
            image_bytes = io.BytesIO()
            pil_image.save(image_bytes, format="JPEG")
            image_bytes_list.append(image_bytes.getvalue())
        return [
            StreamingResponse(iter([image_bytes]), media_type="image/jpeg")
            for image_bytes in image_bytes_list
        ]
