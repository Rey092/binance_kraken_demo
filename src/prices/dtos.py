"""Ninja Pydantic DTOs for the prices app."""

from ninja import Field
from ninja import Schema

from src.prices.enums import PriceExchange


class PricesFiltersDTO(Schema):
    """Prices filters DTO."""

    exchange: PriceExchange | None = Field(default=None, description="Exchange name.")
    pair: str | None = Field(default=None, description="Trading pair. Example: ETHJPY")


class PriceTickerReadDTO(Schema):
    """Price ticker read DTO."""

    exchange: PriceExchange | None = Field(
        default=None,
        description="Exchange name. If None, it's an aggregated "
        "price from multiple exchanges.",
    )
    pair: str = Field(description="Trading pair. Example: ETHYL")
    avg_price: float = Field(
        description="Average price of the pair. "
        "Calculated as (buy_price + sell_price) / 2.",
    )
    buy_price: float = Field(description="Best bid price.")
    sell_price: float = Field(description="Best ask price.")
