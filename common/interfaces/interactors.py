"""Interactor interfaces module."""

from abc import ABC
from abc import abstractmethod
from typing import Generic

from common.types import InputModelT
from common.types import OutputModelT


class Interactor(Generic[InputModelT, OutputModelT], ABC):
    """Interface for interactors."""

    @abstractmethod
    def __call__(self, request_model: InputModelT) -> OutputModelT:
        """Execute the interactor."""
        ...
