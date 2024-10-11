"""Base Price Worker."""

import logging
import threading
import time
from abc import ABC
from typing import TYPE_CHECKING

from websockets.sync.client import connect

from common.interfaces.repositories import IFetchPricesRepository
from common.interfaces.repositories import IStorePricesRepository
from common.interfaces.workers import IPriceWorker
from src.prices.enums import PriceExchange

if TYPE_CHECKING:
    from src.prices.datastructures.price_ticker import PriceTicker

logger = logging.getLogger(__name__)


class WebSocketPriceWorkerBase(threading.Thread, IPriceWorker, ABC):
    """Base class for WebSocket price workers."""

    exchange: PriceExchange

    def __init__(self, ws_url: str, repository: IStorePricesRepository) -> None:
        """Initialize the WebSocket price worker."""
        super().__init__()
        self._ws_url = ws_url
        self._repository = repository
        self._message_price_received = "Received price: {ticker}"
        self._message_subscribed = "Subscribed to {exchange} WebSocket feed."
        self._message_worker_started = "Starting {exchange} worker."
        self._message_error = "Exception in {exchange} worker: {exception}"
        self._message_restart = "Restarting {exchange} worker in 5 seconds..."

    def fetch_prices(self) -> None:
        """Fetch prices from the WebSocket feed."""
        with connect(self._ws_url) as websocket:
            self.subscribe(websocket=websocket)
            logging.info(self._message_subscribed.format(exchange=self.exchange))
            while True:
                message = websocket.recv()
                tickers: list[PriceTicker] = self.parse_message(message)
                if not tickers:
                    continue
                for ticker in tickers:
                    logger.info(self._message_price_received.format(ticker=ticker))
                    self._repository.store_price(ticker=ticker)

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
