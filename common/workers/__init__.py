from abc import ABC, abstractmethod


class PriceWorkerInterface(ABC):
    @abstractmethod
    def run(self):
        """Run the worker to fetch prices from the exchange."""
        pass
