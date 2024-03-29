import logging
import os
from typing import Any, List

from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

from fastserve.core import FastServe

# Configure logger
logger = logging.getLogger(__name__)


class PromptRequest(BaseModel):
    prompt: str = "Write a python function to resize image to 224x224"
    temperature: float = 0.8
    top_p: float = 1.0
    max_tokens: int = 200
    stop: List[str] = []


class ServeHuggingFace(FastServe):
    def __init__(
        self, model_name: str = None, use_gpu: bool = False, device="cpu", **kwargs
    ):
        # Determine execution mode from environment or explicit parameter
        self.use_gpu = use_gpu or os.getenv("USE_GPU", "false").lower() in ["true", "1"]
        self.device = device

        # HF authentication
        hf_token = os.getenv("HUGGINGFACE_TOKEN")
        if hf_token:
            from huggingface_hub import HfFolder

            HfFolder.save_token(
                hf_token
            )  # This saves the token to the Hugging Face configuration folder
        else:
            print(
                "Environment variable 'HUGGINGFACE_TOKEN' not set. It can be necessary to download some models from Hugging Face Hub."
            )

        self.model, self.tokenizer = self._load_model_and_tokenizer(
            model_name or os.getenv("HUGGINGFACE_MODEL_NAME")
        )
        super().__init__(**kwargs)

    def _load_model_and_tokenizer(self, model_name: str):
        if not model_name:
            logger.error(
                "The Hugging Face model name has not been provided. \
                    It must be set either as an environment variable 'HUGGINGFACE_MODEL_NAME' \
                    or passed as an argument during class instantiation."
            )
            return None, None
        try:
            if self.use_gpu:
                # Load model with GPU support, device_map="auto" enables multi-GPU if available
                model = AutoModelForCausalLM.from_pretrained(
                    model_name, device_map="auto"
                )
            else:
                # Load model for CPU execution
                model = AutoModelForCausalLM.from_pretrained(model_name)

            tokenizer = AutoTokenizer.from_pretrained(model_name)
            logger.info(f"Model and tokenizer for '{model_name}' loaded successfully.")
            return model, tokenizer
        except Exception as e:
            logger.error(
                f"Failed to load model and tokenizer '{model_name}'. Error: {e}"
            )
            return None, None

    def __call__(self, request: PromptRequest) -> Any:
        try:
            inputs = self.tokenizer.encode(request.prompt, return_tensors="pt")

            if self.use_gpu:
                inputs = inputs.to(self.device)

            output = self.model.generate(
                inputs,
                max_length=request.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
            )
            text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            logger.info(f"Generated text: {text}")
            return text
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return ""

    def handle(self, batch: List[PromptRequest]) -> List:
        responses = [self(request) for request in batch]
        return responses
