"""Kraken WebSocket worker."""

import json
from typing import Any

import httpx
import websockets

from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange
from src.prices.workers import WebSocketPriceWorkerBase


class KrakenWorker(WebSocketPriceWorkerBase):
    """Kraken WebSocket price worker."""

    exchange: PriceExchange = PriceExchange.kraken
    _kraken_symbols_url = "https://api.kraken.com/0/public/AssetPairs"
    _kraken_subscribe_batch_size = 500

    def parse_message(self, message: str) -> list[PriceTicker]:
        """Parse Kraken WebSocket messages."""
        payload = json.loads(message)
        data_array = payload.get("data", [[]])
        data: dict[str, Any] = data_array[0]

        if not isinstance(data, dict) or not data.get("symbol"):
            return []

        pair: str = data["symbol"]
        buy_price = float(data["high"])
        sell_price = float(data["low"])

        return [
            PriceTicker(
                exchange=self.exchange,
                pair=pair,
                buy_price=buy_price,
                sell_price=sell_price,
            ),
        ]

    def subscribe(self, websocket: websockets.WebSocketClientProtocol):
        """Subscribe to the Kraken WebSocket feed.

        Kraken has a symbols' limit for subscription,
        but it's possible to send subscription requests in batches
        and subscribe to all symbols this way.
        """
        symbols = self._get_all_symbols()
        for i in range(0, len(symbols), self._kraken_subscribe_batch_size):
            websocket.send(
                json.dumps(
                    {
                        "method": "subscribe",
                        "params": {
                            "channel": "ticker",
                            "symbol": symbols[
                                i : i + self._kraken_subscribe_batch_size
                            ],
                        },
                    },
                ),
            )

    def _get_all_symbols(self) -> list[str]:
        """Retrieve all Kraken trading pairs."""
        response = httpx.get(self._kraken_symbols_url)
        data = response.json()
        pairs = data.get("result", {})
        return [pair.get("wsname") for pair in pairs.values() if pair.get("wsname")]
