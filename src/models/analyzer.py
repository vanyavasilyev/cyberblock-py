from abc import ABC, abstractmethod
from typing import Any


class AnalyzerInterface(ABC):
    @abstractmethod
    def run_command(self, command: str, args: Any):
        pass
