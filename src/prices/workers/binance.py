"""Binance WebSocket price worker."""

import json

from websockets.sync.client import ClientConnection

from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange
from src.prices.workers import WebSocketPriceWorker


class BinanceWebSocketPriceWorker(WebSocketPriceWorker):
    """Binance WebSocket price worker."""

    exchange: PriceExchange = PriceExchange.binance

    def parse_message(self, message: str) -> list[PriceTicker]:
        """Parse Binance WebSocket message.

        Extract to a PriceTicker list.
        """
        payload = json.loads(message)
        data = payload.get("data", [])

        if not data:
            return []

        prices: list[PriceTicker] = []

        for item in data:
            pair = item.get("s")
            buy_price = float(item.get("b"))  # Best bid price
            sell_price = float(item.get("a"))  # Best ask price
            prices.append(
                PriceTicker(
                    exchange=self.exchange,
                    pair=pair,
                    buy_price=buy_price,
                    sell_price=sell_price,
                ),
            )

        return prices

    def subscribe(self, websocket: ClientConnection):
        """Subscribe to the Binance WebSocket feed."""
        subscribe_message = json.dumps(
            {"method": "SUBSCRIBE", "params": ["!ticker@arr"], "id": 1},
        )
        websocket.send(subscribe_message)
