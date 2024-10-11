"""Base Price Worker."""

import asyncio
import logging
import threading
import time

from websockets import WebSocketClientProtocol
from websockets.sync.client import ClientConnection
from websockets.sync.client import connect

from common.interfaces.price_service import PriceServiceInterface
from common.interfaces.price_worker import PriceWorkerInterface
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange

logger = logging.getLogger(__name__)


class WebSocketPriceWorker(PriceWorkerInterface, threading.Thread):
    """Base class for WebSocket price workers."""

    exchange: PriceExchange

    def __init__(self, ws_url: str, price_service: PriceServiceInterface) -> None:
        """Initialize the WebSocket price worker."""
        super().__init__()
        self.ws_url = ws_url
        self.price_service = price_service
        self._message_price_received = "Received price: {ticker}"
        self._message_subscribed = "Subscribed to {exchange} WebSocket feed."
        self._message_worker_started = "Starting {exchange} worker."
        self._message_error = "Exception in {exchange} worker: {exception}"
        self._message_restart = "Restarting {exchange} worker in 5 seconds..."

    def fetch_prices(self) -> None:
        """Fetch prices from the WebSocket feed."""
        with connect(self.ws_url) as websocket:
            self.subscribe(websocket=websocket)
            logging.info(self._message_subscribed.format(exchange=self.exchange))
            while True:
                message = websocket.recv()
                tickers: list[PriceTicker] = self.parse_message(message)
                if not tickers:
                    continue
                for ticker in tickers:
                    logger.info(self._message_price_received.format(ticker=ticker))
                    self.price_service.store_price(ticker=ticker)

    def parse_message(self, message: str) -> list[PriceTicker]:
        """Parse the message from the exchange. Return a list of PriceTicker objects."""
        raise NotImplementedError

    def subscribe(self, websocket: ClientConnection) -> None:
        """Subscribe to the WebSocket feed."""
        raise NotImplementedError

    def run(self) -> None:
        """Run the worker in a thread."""
        logger.info(self._message_worker_started.format(exchange=self.exchange))
        while True:
            try:
                self.fetch_prices()
            except Exception as exception:
                message = (
                    self._message_error.format(
                        exchange=self.exchange,
                        exception=exception,
                    ),
                )
                logger.exception(message)
                logger.info(self._message_restart.format(exchange=self.exchange))
                time.sleep(5)
