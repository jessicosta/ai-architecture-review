from abc import ABC, abstractmethod
from typing import Iterator


class LLMClient(ABC):
    """
    Abstract base class for LLM providers.
    Implementations must stream text chunks.
    """

    @abstractmethod
    def generate(self, prompt: str) -> Iterator[str]:
        pass