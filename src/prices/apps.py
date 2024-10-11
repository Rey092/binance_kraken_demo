"""Prices app configuration."""

from django.apps import AppConfig

from src.prices.repositories.prices import PriceRepository
from src.prices.workers.binance import BinanceWebSocketPriceWorker
from src.prices.workers.kraken import KrakenWorker


class PricesConfig(AppConfig):
    """Prices app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.prices"

    def ready(self):
        """Start the price workers."""
        # initialize the price repository
        repository = PriceRepository()

        # Start the Binance price worker's thread
        binance_worker = BinanceWebSocketPriceWorker(
            ws_url="wss://stream.binance.com:9443/stream?streams=",
            repository=repository,
        )
        binance_worker.start()

        # Start the Kraken price worker's thread
        kraken_worker = KrakenWorker(
            ws_url="wss://ws.kraken.com/v2",
            repository=repository,
        )
        kraken_worker.start()
