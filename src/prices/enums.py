"""Enums for the prices' app."""

from enum import StrEnum


class PriceExchange(StrEnum):
    """Exchanges supported by the price service."""

    binance = "binance"
    kraken = "kraken"
