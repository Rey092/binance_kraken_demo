from dataclasses import dataclass

from src.prices.enums import PriceExchanges


@dataclass
class PriceTicker:
    """Price ticker dataclass."""

    exchange: PriceExchanges
    pair: str
    buy_price: float
    sell_price: float

    def __str__(self):
        return f"Exchange: {self.exchange}, Pair: {self.pair}, Avg Price: {self.avg_price}"

    @property
    def avg_price(self):
        """Calculate the average price."""
        return (self.buy_price + self.sell_price) / 2

    def __post_init__(self):
        """Normalize the pair name. Adjust prices to 7 decimal places."""
        self.pair = self.pair.replace("/", "").replace(":", "").upper()
        self.buy_price = round(self.buy_price, 7)
        self.sell_price = round(self.sell_price, 7)
