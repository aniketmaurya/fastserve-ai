import random
import time
import uuid
from dataclasses import dataclass, field
from queue import Empty, Queue
from threading import Event, Thread
from typing import Any, Callable, Dict, List

from logging import Logger, INFO

logger = Logger(__name__, level=INFO)


class BatchedQueue:
    def __init__(self, timeout=1.0, bs=1):
        self.timeout = timeout
        self.bs = bs
        self._queue: Queue = Queue()
        self._result = []
        self._event = Event()

    def get(self):
        entered_at = time.time()
        timeout = self.timeout
        bs = self.bs

        if self._queue.qsize() >= bs:
            return [self._queue.get_nowait() for _ in range(bs)]

        while (
            self._event.wait(timeout - (time.time() - entered_at))
            and self._queue.qsize() < bs
        ):
            True

        result = []
        try:
            for _ in range(bs):
                result.append(self._queue.get_nowait())
            return result
        except Empty:
            return result

    def put(self, item):
        self._queue.put(item)
        if self._event.is_set() and self.size >= self.bs:
            self._event.set()

    @property
    def size(self):
        return self._queue.qsize()


@dataclass
class WaitedObject:
    item: Any = None
    result: Any = None
    _event: Event = None
    created_at: float = field(default_factory=lambda: time.time())
    completed_at: float = None

    def __post_init__(self):
        self._event = Event()

    def set_result(self, result) -> None:
        self.result = result
        self.completed_at = time.time()
        self._event.set()

    @property
    def completed(self) -> bool:
        return self._event.is_set()

    @property
    def completion_time(self) -> str:
        if self.completed_at:
            return f"{self.completed_at - self.created_at:.3f}s"
        else:
            return "Waiting"

    def get(self, timeout: float = None) -> Any:
        if self.completed:
            return self.result
        self._event.wait(timeout)
        return self.result

    def __repr__(self) -> str:
        return f"WaitedOjb({dict(item=self.item, completed=self.completed, result=self.result, completion_time=self.completion_time)})"


class BatchProcessor:
    def __init__(
        self,
        func: Callable,
        timeout=4.0,
        bs=1,
    ):
        self._batched_queue = BatchedQueue(timeout=timeout, bs=bs)
        self.func = func
        self._event = Event()
        self._cancel_signal = Event()

        self._thread = Thread(target=self._process_queue)
        self._thread.start()

    def _process_queue(self):
        logger.info("Started processing")
        while True:
            if self._cancel_signal.is_set():
                logger.info("Stopped batch processor")
                return
            t0 = time.time()
            batch: List[WaitedObject] = self._batched_queue.get()
            logger.debug(batch)
            t1 = time.time()
            logger.debug(f"waited {t1-t0:.2f}s for batch")
            if not batch:
                logger.debug("no batch")
                continue
            batch_items = [b.item for b in batch]
            logger.debug(batch_items)
            results = self.func(batch_items)
            if not isinstance(results, list):
                logger.error(f"returned results must be List but is {type(results)}")
            logger.debug(results)
            for b, result in zip(batch, results):
                b.set_result(result)

    def process(self, item: Any):
        waited_obj = WaitedObject(item=item)
        self._batched_queue.put(waited_obj)
        return waited_obj

    def cancel(self):
        self._cancel_signal.set()
        self._thread.join()
