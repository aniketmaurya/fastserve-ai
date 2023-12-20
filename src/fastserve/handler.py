import os
import random
from abc import abstractmethod
from typing import List

import uactor

from fastserve.utils import BaseRequest


class BaseHandler:
    def create_model(self):
        raise NotImplementedError("You must implement create_model.")

    @abstractmethod
    def handle(self, batch: List[BaseRequest]):
        raise NotImplementedError("You must implement handle to run a server.")


class ParallelHandler(BaseHandler, uactor.Actor):
    """This is a Parallel handler"""


class DummyHandler(BaseHandler):
    def create_model(self):
        self.model = lambda x: 1

    def handle(self, batch: List[BaseRequest]) -> List[int]:
        print(f"Hello from subprocess {os.getpid()}!")
        return [random.randint(1, 10)] * len(batch)


if __name__ == "__main__":
    print(f"Hello from main process {os.getpid()}!")
    handler = DummyHandler()
    result = handler.handle([BaseRequest(request=1)])
    print(result)
