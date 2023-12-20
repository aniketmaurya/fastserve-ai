import logging
import signal
import time
from dataclasses import dataclass, field
from queue import Empty, Queue
from threading import Event, Thread
from typing import Any, Callable, List

logger = logging.getLogger(__name__)


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
    _result: Any = None
    _event: Event = None
    created_at: float = field(default_factory=lambda: time.time())
    completed_at: float = None

    def __post_init__(self):
        self._event = Event()

    def set_result(self, result) -> None:
        self._result = result
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
            if isinstance(self._result, Exception):
                raise self._result
            return self._result
        self._event.wait(timeout)
        if isinstance(self._result, Exception):
            raise self._result
        return self._result

    def __repr__(self) -> str:
        d = dict(
            item=self.item,
            completed=self.completed,
            result=self._result,
            completion_time=self.completion_time,
        )
        return f"WaitedOjb({d})"


class BatchProcessor:
    def __init__(
        self,
        func: Callable,
        timeout=4.0,
        bs=1,
    ):
        self._batched_queue = BatchedQueue(timeout=timeout, bs=bs)
        self.func = func
        self._cancel_processing = Event()
        signal.signal(signal.SIGINT, self.cancel)

        self._thread = Thread(target=self._process_queue, daemon=True)
        self._thread.start()

    def _process_queue(self):
        logger.info("Started processing")
        while True:
            if self._cancel_processing.is_set():
                logger.info("Stopped processing")
                return
            t0 = time.time()
            batch: List[WaitedObject] = self._batched_queue.get()
            logger.debug(batch)
            t1 = time.time()
            if not batch:
                logger.debug("no batch")
                continue
            logger.info(f"Aggregated batch size {len(batch)} in {t1 - t0:.2f}s")
            batch_items = [b.item for b in batch]
            logger.debug(batch_items)
            try:
                results = self.func(batch_items)
            except Exception as e:
                logger.error(f"Error while processing batch {batch}")
                logger.exception(e)
                results = [e] * len(batch)
            if not isinstance(results, list):
                logger.error(f"returned results must be List but is {type(results)}")
            logger.debug(results)
            for b, result in zip(batch, results):
                b.set_result(result)

    def process(self, item: Any):
        """Puts the `item` to Queue and consumes batch for processing."""
        waited_obj = WaitedObject(item=item)
        self._batched_queue.put(waited_obj)
        return waited_obj

    def cancel(self, sig=None, frame=None):
        """Cancel batch processing and act as signal handler."""
        logger.warning("Received signal to terminate the thread.")
        logger.info("Terminating Batch Processor...")
        self._cancel_processing.set()
        self._thread.join()
        logger.info("Batch Processor terminated!")
