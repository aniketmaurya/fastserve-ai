from .batching import BatchProcessor
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from .models.llama_cpp import LlamaCppLLM


class PromptRequest(BaseModel):
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 60
    stop: List[str] = []


app = FastAPI()
llm = LlamaCppLLM()
batch_processing = BatchProcessor(func=llm)


@app.post("/serve")
def serve(prompt: PromptRequest):
    batch_processing.process()
    result = llm(
        prompt=prompt,
        temperature=prompt.temperature,
        max_tokens=prompt.max_tokens,
        stop=prompt.stop,
    )
    return result
