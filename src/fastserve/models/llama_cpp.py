import os
from pathlib import Path
from typing import Any

from llama_cpp import Llama
from loguru import logger

# https://huggingface.co/TheBloke/OpenHermes-2-Mistral-7B-GGUF
DEFAULT_MODEL = "openhermes-2-mistral-7b.Q6_K.gguf"


class LlamaCppLLM:
    def __init__(
        self,
        model_path=DEFAULT_MODEL,
        main_gpu=1,
        n_ctx=1028,
        lazy=False,
        *args,
        **kwargs,
    ):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"{model_path} not found.")
        if lazy:
            self.llm = None
        else:
            self.llm = Llama(
                model_path=model_path,
                main_gpu=main_gpu,
                n_ctx=n_ctx,
                verbose=False,
                *args,
                **kwargs,
            )
        self.n_ctx = n_ctx
        self.model_path = model_path
        self.main_gpu = main_gpu
        self.args = args
        self.kwargs = kwargs

    def __call__(self, prompt: str, *args: Any, **kwargs: Any) -> Any:
        if self.llm is None:
            logger.info("Initializing model")
            self.llm = Llama(
                model_path=self.model_path,
                main_gpu=self.main_gpu,
                n_ctx=self.n_ctx,
                verbose=False,
                *self.args,
                **self.kwargs,
            )

        result = self.llm(prompt=prompt, *args, **kwargs)
        logger.info(result)
        return result
