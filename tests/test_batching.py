import random

from fastserve.batching import BatchProcessor


def fake_ml_api(X):
    # print(f"{n} items")
    for i in range(1000):
        for j in range(1000):
            for k in range(50):
                pass

    return [x * random.randint(0, 10) for x in X]


def test_batch_processor():
    p = BatchProcessor(fake_ml_api)
    x = 1
    wait = p.process(x)
    assert wait.completed is False
    result = wait.get()
    assert wait.completed
    assert isinstance(result, (int, float))
    p.cancel()
    assert p._cancel_processing.is_set()
