"""Views for the price app."""

from django.http import HttpRequest
from ninja import Query
from ninja import Router

from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.dtos import PricesFiltersDTO
from src.prices.dtos import PriceTickerReadDTO
from src.prices.interactors.get_prices import GetPricesInteractor
from src.prices.interactors.get_prices import GetPricesRequestModel
from src.prices.interactors.get_prices import GetPricesResponseModel
from src.prices.repositories.prices import PriceRepository

prices_router = Router()


@prices_router.get(
    "/",
    response={200: list[PriceTickerReadDTO]},
    tags=["prices"],
)
def list_prices(
    request: HttpRequest,
    filters: Query[PricesFiltersDTO],
) -> list[PriceTicker]:
    """List prices from the exchanges."""
    # TODO: add dependency injection
    price_repository = PriceRepository()
    price_interactor = GetPricesInteractor(price_repository=price_repository)
    response_model: GetPricesResponseModel = price_interactor(
        request_model=GetPricesRequestModel(
            exchange=filters.exchange,
            pair=filters.pair,
        ),
    )
    return response_model.prices
