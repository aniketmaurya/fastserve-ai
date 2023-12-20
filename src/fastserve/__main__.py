from fastserve import BaseFastServe
from fastserve.handler import DummyHandler

handler = DummyHandler()
serve = BaseFastServe(handler=handler)
serve.run_server()
