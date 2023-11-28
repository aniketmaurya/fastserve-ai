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
llm = LlamaCppLLM(model_path="openhermes-2-mistral-7b.Q5_K_M.gguf")


@app.post("/serve")
def serve(prompt: PromptRequest):
    result = llm(
        prompt=prompt.prompt,
        temperature=prompt.temperature,
        max_tokens=prompt.max_tokens,
        stop=prompt.stop,
    )
    return result
