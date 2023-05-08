from abc import ABC, abstractmethod
from typing import Any, Generator, Union
from .graph import AddressNode, TransactionEdge


class DBDriverInterface(ABC):
    @abstractmethod
    def _close(self, *_):
        pass

    def __enter__(self):
        return self
    
    def __exit__(self, *_):
        self._close()
        return False
    
    @abstractmethod
    def query(self, query: Any, **kwargs):
        pass

    @abstractmethod
    def load(self, data_generator: Generator[Union[AddressNode, TransactionEdge], None, None]):
        pass
