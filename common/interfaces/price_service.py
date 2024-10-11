from abc import ABC, abstractmethod
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange


class PriceServiceInterface(ABC):
    """Interface for storing and retrieving prices from different exchanges."""

    exchange_name: PriceExchange

    @abstractmethod
    def store_price(self, ticker: PriceTicker):
        """Store the price for a given exchange and trading pair."""
        pass

    @abstractmethod
    def get_all_prices(self, exchange: PriceExchange | None):
        """Retrieve all prices from the cache."""
        pass

    @abstractmethod
    def get_price(self, exchange_name: PriceExchange, pair: str):
        """Retrieve the price for a given pair in the specified exchange."""
        pass
