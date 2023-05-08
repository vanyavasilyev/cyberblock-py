from abc import ABC, abstractmethod
from typing import Optional, Generator, Union
from .graph import AddressNode, TransactionEdge


class ScannerInterface(ABC):
    @abstractmethod
    def scan_from(self, address: str,
                  max_iterations: Optional[int] = None
        ) -> Generator[Union[AddressNode, TransactionEdge], None, None]:
        pass
