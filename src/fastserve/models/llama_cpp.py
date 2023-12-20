import logging
import os
from typing import Any, List, Optional

from llama_cpp import Llama
from pydantic import BaseModel

from fastserve import FastServe

logger = logging.getLogger(__name__)

# https://huggingface.co/TheBloke/OpenHermes-2-Mistral-7B-GGUF
DEFAULT_MODEL = "openhermes-2-mistral-7b.Q6_K.gguf"


class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 1
    max_tokens: int = 200
    stop: List[str] = []


class ResponseModel(BaseModel):
    prompt: str
    prompt_token_ids: Optional[List] = None  # The token IDs of the prompt.
    text: str  # The output sequences of the request.
    finished: bool  # Whether the whole request is finished.


class ServeLlamaCpp(FastServe):
    def __init__(
        self,
        model_path=DEFAULT_MODEL,
        batch_size=1,
        timeout=0.0,
        main_gpu=1,
        n_ctx=1028,
        lazy=False,
        *args,
        **kwargs,
    ):
        super().__init__(self, batch_size, timeout, input_schema=PromptRequest)

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

    def handle(self, batch: List[PromptRequest]) -> List[ResponseModel]:
        responses = []
        for item in batch:
            output = self(item.prompt)

            response = ResponseModel(
                **{
                    "prompt": item.prompt,
                    "text": output["choices"][0]["text"],
                    "finished": True,
                }
            )
            responses.append(response)

        return responses
