import logging
from contextlib import asynccontextmanager
from typing import Callable, Optional

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .batching import BatchProcessor
from .handler import BaseHandler, ParallelHandler
from .middleware import register_default_middlewares
from .utils import BaseRequest

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class BaseServe:
    def __init__(
        self,
        handle: Callable,
        batch_size: int,
        timeout: float,
        input_schema: Optional[BaseModel],
        response_schema: Optional[BaseModel],
        ui_mount_static_files: Optional[dict] = {},
    ) -> None:
        self.input_schema = input_schema
        self.response_schema = response_schema
        self.handle: Callable = handle
        self.batch_processing = BatchProcessor(
            func=self.handle, bs=batch_size, timeout=timeout
        )
        self.ui_mount_static_files = ui_mount_static_files

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            self.batch_processing.cancel()

        self._app = FastAPI(lifespan=lifespan, title="FastServe", docs_url="/")
        register_default_middlewares(self._app)
        INPUT_SCHEMA = input_schema

        def api(request: INPUT_SCHEMA):
            print("incoming request")
            wait_obj = self.batch_processing.process(request)
            result = wait_obj.get()
            return result

        self._app.add_api_route(
            path="/endpoint",
            endpoint=api,
            methods=["post"],
            response_model=response_schema,
        )
        for path, directory in self.ui_mount_static_files.items():
            static_files = StaticFiles(
                directory=directory,
            )
            self._app.mount(path, static_files, name=path)
        if self.ui_mount_static_files:
            logger.info(f"Mounted UI routes: {self.ui_mount_static_files}")

            @self._app.get("/ui")
            def home():
                return RedirectResponse("/static/index.html")

    @property
    def app(self):
        return self._app

    def run_server(
        self,
    ):
        import uvicorn

        uvicorn.run(self.app)

    @property
    def test_client(self):
        from fastapi.testclient import TestClient

        return TestClient(self._app)


class FastServe(BaseServe, BaseHandler):
    def __init__(
        self,
        batch_size=2,
        timeout=0.5,
        input_schema=None,
        response_schema=None,
        ui_mount_static_files={},
    ):
        if input_schema is None:
            input_schema = BaseRequest
        super().__init__(
            handle=self.handle,
            batch_size=batch_size,
            timeout=timeout,
            input_schema=input_schema,
            response_schema=response_schema,
            ui_mount_static_files=ui_mount_static_files,
        )


class ParallelFastServe(BaseServe, ParallelHandler):
    def __init__(
        self, batch_size=2, timeout=0.5, input_schema=None, response_schema=None
    ):
        if input_schema is None:
            input_schema = BaseRequest
        super().__init__(
            handle=self.handle,
            batch_size=batch_size,
            timeout=timeout,
            input_schema=input_schema,
            response_schema=response_schema,
        )
        logger.info("Launching parallel handler!")
