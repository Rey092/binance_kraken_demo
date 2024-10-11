from abc import ABC, abstractmethod
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchanges


class PriceServiceInterface(ABC):
    """Interface for storing and retrieving prices from different exchanges."""

    exchange_name: PriceExchanges

    @abstractmethod
    def store_price(self, ticker: PriceTicker):
        """Store the price for a given exchange and trading pair."""
        pass

    @abstractmethod
    def get_all_prices(self, exchange: PriceExchanges | None):
        """Retrieve all prices from the cache."""
        pass

    @abstractmethod
    def get_price(self, exchange_name: PriceExchanges, pair: str):
        """Retrieve the price for a given pair in the specified exchange."""
        pass
