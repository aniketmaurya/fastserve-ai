import os
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from vllm import LLM, SamplingParams

tensor_parallel_size = int(os.environ.get("DEVICES", "1"))
print("tensor_parallel_size: ", tensor_parallel_size)

llm = LLM("meta-llama/Llama-2-7b-hf", tensor_parallel_size=tensor_parallel_size)


class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 1
    max_tokens: int = 200
    stop: List[str] = []


class ResponseModel(BaseModel):
    prompt: str
    prompt_token_ids: List  # The token IDs of the prompt.
    outputs: List[str]  # The output sequences of the request.
    finished: bool  # Whether the whole request is finished.


app = FastAPI()


@app.post("/serve", response_model=ResponseModel)
def serve(request: PromptRequest):
    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        stop=request.stop,
    )

    result = llm.generate(request.prompt, sampling_params=sampling_params)[0]
    response = ResponseModel(
        prompt=request.prompt,
        prompt_token_ids=result.prompt_token_ids,
        outputs=result.outputs,
        finished=result.finished,
    )
    return response
