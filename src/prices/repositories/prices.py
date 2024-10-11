"""Price repository to store and retrieve prices."""

import threading

from django.core.cache import cache

from common.interfaces.repositories import IGetPricesRepository
from common.interfaces.repositories import IStorePricesRepository
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange
from src.prices.exceptions import PriceNotFoundError


class PriceRepository(
    IStorePricesRepository,
    IGetPricesRepository,
):
    """Repository to store and retrieve prices."""

    _lock = threading.Lock()

    def __init__(self):
        """Initialize the price service."""
        self._exception_invalid_exchange = (
            "Invalid exchange: {ticker_exchange}. Expected: {service_exchange}"
        )
        self._key_for_keys = "keys:{exchange}"
        self._key_for_ticker = "ticker:{exchange}_{pair}"

    def store_price(self, ticker: PriceTicker):
        """Store the price in the cache."""
        cache_key = self._key_for_ticker.format(
            exchange=ticker.exchange,
            pair=ticker.pair,
        )

        with self._lock:
            # Store the price in the cache
            cache.set(cache_key, ticker, timeout=None)

            # Get the current set of cache keys atomically
            cache_keys = cache.get(self._key_for_keys.format(exchange=ticker.exchange))
            if cache_keys is None:
                cache_keys = set()

            # Add the new cache key and update the cache atomically
            cache_keys.add(cache_key)

            # Pipeline to avoid race conditions (if using Redis)
            cache.set(
                self._key_for_keys.format(exchange=ticker.exchange),
                cache_keys,
                timeout=None,
            )

    def get_all_prices(self, exchange: PriceExchange | None) -> list[PriceTicker]:
        """Retrieve all prices from the cache."""
        cache_keys = self._prepare_cache_keys_for_prices(exchange)
        price_tickers: list[PriceTicker] = list(cache.get_many(cache_keys).values())

        # if exchange is provided, return the list of prices
        if exchange:
            price_tickers.sort(key=lambda x: x.pair)
            return price_tickers

        # Group by pair
        grouped_data: dict[str, list[PriceTicker]] = {}
        for ticker in price_tickers:
            grouped_data.setdefault(ticker.pair, []).append(ticker)

        # Create aggregated data if exchange is not provided
        aggregated_data = [
            PriceTicker.aggregate(price_tickers=tickers)
            for tickers in grouped_data.values()
        ]

        # Sort the aggregated data by pair
        aggregated_data.sort(key=lambda x: x.pair)

        return aggregated_data

    def _prepare_cache_keys_for_prices(
        self,
        exchange: PriceExchange | None,
    ) -> set[str]:
        """Prepare the cache keys for the prices."""
        if exchange:
            cache_keys: set[str] = cache.get(
                self._key_for_keys.format(exchange=exchange),
                set(),
            )
        else:
            exchange_names = PriceExchange.__members__.keys()
            cache_keys_map: dict[str, set[str]] = cache.get_many(
                [
                    self._key_for_keys.format(exchange=exchange.lower())
                    for exchange in exchange_names
                ],
            )
            cache_keys = {key for keys in cache_keys_map.values() for key in keys}
        return cache_keys

    def get_price(
        self,
        pair: str,
        exchange: PriceExchange | None = None,
    ) -> PriceTicker:
        """Retrieve the price for a given pair."""
        if exchange:
            ticker = cache.get(
                self._key_for_ticker.format(exchange=exchange, pair=pair),
            )
        else:
            exchanges_names = PriceExchange.__members__.keys()
            tickers: list[PriceTicker] = list(
                cache.get_many(
                    [
                        self._key_for_ticker.format(exchange=exchange, pair=pair)
                        for exchange in exchanges_names
                    ],
                ).values(),
            )

            if not tickers:
                raise PriceNotFoundError

            ticker = PriceTicker.aggregate(price_tickers=tickers)

        if not ticker:
            raise PriceNotFoundError

        return ticker
