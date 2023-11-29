from typing import Any, List

from fastapi import FastAPI
from pydantic import BaseModel

from .batching import BatchProcessor


class BaseRequest(BaseModel):
    request: Any


class FastServe:
    def __init__(self, batch_size=2, timeout=0.5) -> None:
        self.batch_processing = BatchProcessor(
            func=self.handle, bs=batch_size, timeout=timeout
        )
        self._app = FastAPI()

        @self._app.on_event("shutdown")
        def shutdown_event():
            self.batch_processing.cancel()

    def serve(
        self,
    ):
        @self._app.post(path="/endpoint")
        def api(request: BaseRequest):
            wait_obj = self.batch_processing.process(request)
            return wait_obj.get()

    def handle(self, batch: List[BaseRequest]):
        n = len(batch)
        return n * [0.5 * n]

    def run_server(
        self,
    ):
        self.serve()
        import uvicorn

        uvicorn.run(self._app)
