# Note that this model is not commercially licensed
import io
import logging
from typing import List

import torch
from diffusers import AutoPipelineForText2Image
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from fastserve import FastServe
from fastserve.utils import get_ui_folder


class PromptRequest(BaseModel):
    prompt: str  # "An astronaut riding a green horse"
    negative_prompt: str = "ugly, blurry, poor quality"


class ServeSDXLTurbo(FastServe):
    def __init__(
        self, batch_size=1, timeout=0.0, device="cuda", num_inference_steps: int = 1
    ) -> None:
        if num_inference_steps > 1:
            logging.warning(
                "It is recommended to use inference_steps=1 for SDXL Turbo model."
            )
        self.num_inference_steps = num_inference_steps
        self.pipe = AutoPipelineForText2Image.from_pretrained(
            "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16"
        )
        self.pipe.to(device)

        # Mount the UI folder
        ui_path = get_ui_folder()
        ui_mount_static_files = {
            "/static": f"{ui_path}/dist",
            "/assets": f"{ui_path}/dist/assets",
        }

        super().__init__(
            batch_size,
            timeout,
            input_schema=PromptRequest,
            ui_mount_static_files=ui_mount_static_files,
        )

    @torch.inference_mode()
    def handle(self, batch: List[PromptRequest]) -> List[StreamingResponse]:
        prompts = [b.prompt for b in batch]
        negative_prompts = [b.negative_prompt for b in batch]

        pil_images = self.pipe(
            prompt=prompts,
            negative_prompt=negative_prompts,
            num_inference_steps=self.num_inference_steps,
            guidance_scale=0.0,
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
