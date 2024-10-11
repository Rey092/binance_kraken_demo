"""Exceptions for the price's app."""


class PriceNotFoundError(Exception):
    """Exception raised when a price is not found."""

    def __init__(self, message: str = "Price not found.") -> None:
        """Initialize the exception."""
        super().__init__(message)
