import logging
from typing import Any, List, Optional

from pydantic import BaseModel

from fastserve.core import FastServe

logger = logging.getLogger(__name__)


class PromptRequest(BaseModel):
    prompt: str = "Write a python function to resize image to 224x224"
    temperature: float = 0.8
    top_p: float = 1.0
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
        model,
        batch_size=1,
        timeout=0.0,
        *args,
        **kwargs,
    ):
        from vllm import LLM

        self.llm = LLM(model)
        self.args = args
        self.kwargs = kwargs
        super().__init__(
            batch_size,
            timeout,
            input_schema=PromptRequest,
            # response_schema=ResponseModel,
        )

    def __call__(self, request: PromptRequest) -> Any:
        from vllm import SamplingParams

        sampling_params = SamplingParams(
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
        )
        result = self.llm.generate(request.prompt, sampling_params=sampling_params)
        logger.info(result)
        return result

    def handle(self, batch: List[PromptRequest]) -> List:
        responses = []
        for request in batch:
            output = self(request)
            responses.extend(output)

        return responses
