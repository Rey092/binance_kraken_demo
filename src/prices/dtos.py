"""Ninja Pydantic DTOs for the prices app."""
from typing import Self

from ninja import Schema, Field

from src.prices.enums import PriceExchange


class PricesFiltersDTO(Schema):
    """Prices filters DTO."""

    exchange: PriceExchange | None = Field(
        default=None, description="Exchange name."
    )
    pair: str | None = Field(
        default=None, description="Trading pair. Example: ETHJPY"
    )


class PriceTickerReadDTO(Schema):
    """Price ticker read DTO."""

    exchange: PriceExchange | None = Field(
        default=None, description="Exchange name. If None, it's an aggregated price from multiple exchanges."
    )
    pair: str = Field(
        description="Trading pair. Example: ETHYL"
    )
    avg_price: float = Field(
        description="Average price of the pair. Calculated as (buy_price + sell_price) / 2."
    )
