"""Interface for repositories."""

from abc import ABC
from abc import abstractmethod

from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange


class PriceRepositoryInterface(ABC):
    """Interface for storing and retrieving prices from different exchanges."""

    @abstractmethod
    def store_price(
        self,
        ticker: PriceTicker,
    ) -> None:
        """Store the price for a given exchange and trading pair."""

    @abstractmethod
    def get_all_prices(
        self,
        exchange: PriceExchange | None,
    ) -> list[PriceTicker]:
        """Retrieve all prices from the cache."""

    @abstractmethod
    def get_price(
        self,
        pair: str,
        exchange: PriceExchange | None = None,
    ) -> PriceTicker:
        """Retrieve the price for a given pair in the specified exchange."""
