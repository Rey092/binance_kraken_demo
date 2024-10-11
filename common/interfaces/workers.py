"""This module defines the interface for price workers."""

from abc import ABC
from abc import abstractmethod


class PriceWorkerInterface(ABC):
    """Interface for fetching prices from different exchanges."""

    @abstractmethod
    def run(self):
        """Run the worker to fetch prices from the exchange."""