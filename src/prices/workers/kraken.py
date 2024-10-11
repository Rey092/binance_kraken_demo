"""Kraken WebSocket worker."""

import json
import httpx
import websockets
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchanges
from src.prices.workers import WebSocketPriceWorker


class KrakenWorker(WebSocketPriceWorker):
    """Kraken WebSocket price worker."""

    exchange_name = PriceExchanges.kraken
    _kraken_symbols_url = "https://api.kraken.com/0/public/AssetPairs"
    _kraken_subscribe_batch_size = 500

    def parse_message(self, message: str) -> list[PriceTicker]:
        """Parse Kraken WebSocket messages."""
        payload = json.loads(message)
        data_array = payload.get("data", [[]])
        data = data_array[0]

        if not isinstance(data, dict) or not data.get("symbol"):
            return []

        pair = data.get("symbol")
        buy_price = float(data.get("high"))
        sell_price = float(data.get("low"))

        return [PriceTicker(exchange=self.exchange_name, pair=pair, buy_price=buy_price, sell_price=sell_price)]

    def subscribe(self, websocket: websockets.WebSocketClientProtocol):
        """Subscribe to the Kraken WebSocket feed."""
        symbols = self.get_all_symbols()
        for i in range(0, len(symbols), self._kraken_subscribe_batch_size):
            websocket.send(
                json.dumps(
                    {
                        "method": "subscribe",
                        "params":
                            {
                                "channel": "ticker",
                                "symbol": symbols[i:i + self._kraken_subscribe_batch_size]
                            }
                    }
                )
            )

    def get_all_symbols(self) -> list[str]:
        """Retrieve all Kraken trading pairs."""
        response = httpx.get(self._kraken_symbols_url)
        data = response.json()
        pairs = data.get('result', {})
        return [pair.get("wsname") for pair in pairs.values() if pair.get("wsname")]
