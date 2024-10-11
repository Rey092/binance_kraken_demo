"""Aggregated price ticker dataclass."""

from dataclasses import dataclass
from src.prices.datastructures.price_ticker import PriceTicker


@dataclass
class AggregatedPriceTicker:
    """Price ticker dataclass."""

    def __init__(self, price_tickers: list[PriceTicker]):
        """Initialize the price ticker."""
        # all tickers should have the same pair
        if len(set(ticker.pair for ticker in price_tickers)) > 1:
            raise ValueError("All tickers should have the same pair.")
        self.pair = price_tickers[0].pair
        self.buy_price = sum(ticker.buy_price for ticker in price_tickers) / len(price_tickers)
        self.sell_price = sum(ticker.sell_price for ticker in price_tickers) / len(price_tickers)
        self.exchange_data = price_tickers

    def __str__(self):
        """Return the string representation of the price ticker."""
        return f"Aggregated ticker. Pair: {self.pair}, Avg Price: {self.avg_price}"

    @property
    def avg_price(self):
        """Calculate the average price."""
        return (self.buy_price + self.sell_price) / 2
