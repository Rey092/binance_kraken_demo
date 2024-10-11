"""Get prices interactor."""

from dataclasses import dataclass

from common.interfaces.interactors import Interactor
from common.interfaces.repositories import IFetchPricesRepository
from src.prices.datastructures.price_ticker import PriceTicker
from src.prices.enums import PriceExchange


@dataclass
class GetPricesRequestModel:
    """Request model for getting prices."""

    exchange: PriceExchange | None = None
    pair: str | None = None


@dataclass
class GetPricesResponseModel:
    """Response model for getting prices."""

    prices: list[PriceTicker]


class GetPricesInteractor(Interactor[GetPricesRequestModel, GetPricesResponseModel]):
    """Interactor for getting prices from the repositories."""

    def __init__(self, price_repository: IFetchPricesRepository) -> None:
        """Initialize the interactor."""
        self._price_repository = price_repository

    def __call__(self, request_model: GetPricesRequestModel) -> GetPricesResponseModel:
        """Get prices from the repository."""
        if not request_model.pair:
            prices = self._price_repository.get_all_prices(
                exchange=request_model.exchange,
            )
        else:
            prices = [
                self._price_repository.get_price(
                    pair=request_model.pair,
                    exchange=request_model.exchange,
                ),
            ]
        return GetPricesResponseModel(prices=prices)
