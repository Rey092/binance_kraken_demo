"""Views for the price app."""

from ninja import Router, Query

from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.dtos import PricesFiltersDTO, PriceTickerReadDTO
from src.prices.services.prices import PriceService

prices_router = Router()


@prices_router.get('/', response={200: list[PriceTickerReadDTO]}, tags=['prices'])
def list_prices(
    request, filters: Query[PricesFiltersDTO]
) -> list[PriceTicker]:
    """List prices from the exchanges."""
    price_service = PriceService()

    # If neither exchange nor pair is provided, get all prices from both exchanges
    if not filters.pair:
        return price_service.get_all_prices(exchange=filters.exchange)

    # Get one price for the given pair
    return [price_service.get_price(pair=filters.pair, exchange=filters.exchange)]
