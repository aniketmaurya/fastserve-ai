import logging
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI

from .batching import BatchProcessor
from .handler import BaseHandler
from .utils import BaseRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)


class BaseFastServe:
    def __init__(self, handle: Callable, batch_size, timeout, input_schema) -> None:
        self.input_schema = input_schema
        self.handle: Callable = handle
        self.batch_processing = BatchProcessor(
            func=self.handle, bs=batch_size, timeout=timeout
        )

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            self.batch_processing.cancel()

        self._app = FastAPI(lifespan=lifespan, title="FastServe")

    def _serve(
        self,
    ):
        INPUT_SCHEMA = self.input_schema

        @self._app.post(path="/endpoint")
        def api(request: INPUT_SCHEMA):
            print("incoming request")
            wait_obj = self.batch_processing.process(request)
            result = wait_obj.get()
            return result

    def run_server(
        self,
    ):
        self._serve()
        import uvicorn

        uvicorn.run(self._app)

    @property
    def test_client(self):
        from fastapi.testclient import TestClient

        return TestClient(self._app)


class FastServe(BaseFastServe, BaseHandler):
    def __init__(self, batch_size=2, timeout=0.5, input_schema=None):
        if input_schema is None:
            input_schema = BaseRequest
        super().__init__(
            handle=self.handle,
            batch_size=batch_size,
            timeout=timeout,
            input_schema=input_schema,
        )
