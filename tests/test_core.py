import pytest
from fastserve import FastServe
from fastserve.core import BaseRequest


class FakeServe(FastServe):
    def handle(self, batch):
        return [1] * len(batch)


def test_handle():
    serve = FastServe()
    batch = [BaseRequest(request=1), BaseRequest(request=2)]
    with pytest.raises(NotImplementedError):
        serve.handle(batch)

    serve = FakeServe()
    assert serve.handle(batch) == [1, 1]


def test_run_server():
    serve = FakeServe()
    serve._serve()
    test_client = serve.test_client
    data = BaseRequest(request=1).model_dump_json()
    response = test_client.post("/endpoint", data=data)
    assert response.status_code == 200
    assert response.json() == 1


def test_exception():
    serve = FakeServe()
    serve._serve()
    test_client = serve.test_client
    data = {}  # wrong data format
    response = test_client.post("/endpoint", data=data)
    assert response.status_code == 422
