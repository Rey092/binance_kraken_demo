"""Enums for the prices' app."""

from django.db import models


class PriceExchange(models.TextChoices):
    """Exchanges supported by the price service."""

    binance = "binance", "Binance"
    kraken = "kraken", "Kraken"
