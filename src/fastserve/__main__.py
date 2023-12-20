from fastserve.core import BaseFastServe
from fastserve.handler import DummyHandler
from fastserve.utils import BaseRequest

handler = DummyHandler()
serve = BaseFastServe(
    handle=handler.handle, batch_size=1, timeout=0, input_schema=BaseRequest
)
serve.run_server()
