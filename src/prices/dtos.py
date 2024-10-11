"""Ninja Pydantic DTOs for the prices app."""
from typing import Self

from ninja import Schema, Field

from src.prices.enums import PriceExchanges


class PricesFiltersDTO(Schema):
    """Prices filters DTO."""

    exchange: PriceExchanges | None = Field(
        default=None, description="Exchange name."
    )
    pair: str | None = Field(
        default=None, description="Trading pair. Example: ETHJPY"
    )


class PriceTickerReadBaseDTO(Schema):
    """Price ticker read base DTO."""

    pair: str
    avg_price: float


class ExchangePriceTickerReadDTO(PriceTickerReadBaseDTO):
    """Exchange price ticker read DTO."""

    exchange: PriceExchanges


class PriceTickerReadDTO(PriceTickerReadBaseDTO):
    """Price ticker read DTO."""

    exchange_data: list[ExchangePriceTickerReadDTO] = Field(default_factory=list)
