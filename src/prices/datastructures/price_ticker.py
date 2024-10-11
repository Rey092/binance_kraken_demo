"""Price ticker dataclass."""

from dataclasses import dataclass

from src.prices.enums import PriceExchange


@dataclass
class PriceTicker:
    """Price ticker dataclass."""

    exchange: PriceExchange | None
    pair: str
    buy_price: float
    sell_price: float

    def __str__(self):
        """String representation of the price ticker."""
        return (
            f"Exchange: {self.exchange}, Pair: {self.pair}, Avg Price: {self.avg_price}"
        )

    @property
    def avg_price(self):
        """Calculate the average price."""
        return (self.buy_price + self.sell_price) / 2

    def __post_init__(self):
        """Normalize the pair name. Adjust prices to 7 decimal places."""
        self.pair = self.pair.replace("/", "").replace(":", "").upper()
        self.buy_price = round(self.buy_price, 7)
        self.sell_price = round(self.sell_price, 7)

    @classmethod
    def aggregate(cls, tickers: list["PriceTicker"]) -> "PriceTicker":
        """Aggregate multiple price tickers into a single one."""
        if not tickers:
            no_price_tickers = "No price tickers to aggregate."
            raise ValueError(no_price_tickers)
        if len({ticker.pair for ticker in tickers}) > 1:
            all_tickers_same_pair = "All tickers should have the same pair."
            raise ValueError(all_tickers_same_pair)
        return cls(
            exchange=None,
            pair=tickers[0].pair,
            buy_price=sum(ticker.buy_price for ticker in tickers) / len(tickers),
            sell_price=sum(ticker.sell_price for ticker in tickers) / len(tickers),
        )
