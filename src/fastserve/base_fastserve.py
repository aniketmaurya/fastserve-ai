from contextlib import asynccontextmanager
from typing import Any, List

from fastapi import FastAPI
from pydantic import BaseModel

from .batching import BatchProcessor


class BaseRequest(BaseModel):
    request: Any


class FastServe:
    def __init__(self, batch_size=2, timeout=0.5, input_schema=BaseRequest) -> None:
        self.input_schema = input_schema
        self.batch_processing = BatchProcessor(
            func=self.handle, bs=batch_size, timeout=timeout
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            self.batch_processing.cancel()

        self._app = FastAPI(lifespan=lifespan)

    def _serve(
        self,
    ):
        INPUT_SCHEMA = self.input_schema

        @self._app.post(path="/endpoint")
        def api(request: INPUT_SCHEMA):
            wait_obj = self.batch_processing.process(request)
            return wait_obj.get()

    def handle(self, batch: List[BaseRequest]):
        n = len(batch)
        return n * [0.5 * n]

    def run_server(
        self,
    ):
        self._serve()
        import uvicorn

        uvicorn.run(self._app)
