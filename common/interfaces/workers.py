"""This module defines the interface for price workers."""

from abc import abstractmethod
from typing import Protocol

from websockets.sync.client import ClientConnection

from src.prices.datastructures.price_ticker import PriceTicker


class PriceWorkerInterface(Protocol):
    """Interface for fetching prices from different exchanges."""

    @abstractmethod
    def run(self):
        """Run the worker to fetch prices from the exchange."""

    @abstractmethod
    def subscribe(self, websocket: ClientConnection):
        """Subscribe to the WebSocket feed."""

    @abstractmethod
    def parse_message(self, message: str) -> list[PriceTicker]:
        """Parse the message from the exchange. Return a list of PriceTicker objects."""
