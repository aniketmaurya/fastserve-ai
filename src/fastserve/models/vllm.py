import logging
import os
from typing import Any, List, Optional

from llama_cpp import Llama
from pydantic import BaseModel

from fastserve.core import FastServe

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "openhermes-2-mistral-7b.Q6_K.gguf"



class PromptRequest(BaseModel):
    prompt: str = "Llamas are cute animal"
    temperature: float = 0.8
    top_p: float = 0.0
    max_tokens: int = 200
    stop: List[str] = []


class ResponseModel(BaseModel):
    prompt: str
    prompt_token_ids: Optional[List] = None  # The token IDs of the prompt.
    text: str  # The output sequences of the request.
    finished: bool  # Whether the whole request is finished.


class ServeVLLM(FastServe):
    def __init__(
        self,
        model_path=DEFAULT_MODEL,
        batch_size=1,
        timeout=0.0,
        *args,
        **kwargs,
    ):
        from vllm import LLM, SamplingParams

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"{model_path} not found.")
        
        self.llm = LLM(model_path)
        self.model_path = model_path
        self.args = args
        self.kwargs = kwargs
        super().__init__(
            batch_size,
            timeout,
            input_schema=PromptRequest,
            response_schema=ResponseModel,
        )

    def __call__(self, request: PromptRequest) -> Any:
        from vllm import SamplingParams

        sampling_params = SamplingParams(temperature=request.temperature, top_p=request.top_p)
        result = self.llm(request.prompt, sampling_params=sampling_params)
        logger.info(result)
        return result

    def handle(self, batch: List[PromptRequest]) -> List[ResponseModel]:
        responses = []
        for request in batch:
            output = self(request)

            response = ResponseModel(
                **{
                    "prompt": request.prompt,
                    "text": output["choices"][0]["text"],
                    "finished": True,
                }
            )
            responses.append(response)

        return responses
